import gymnasium as gym
from gymnasium import spaces
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np
import pandas as pd
import os
fig, ax = plt.subplots()

class EMSv0_3(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self,bat_threshold = 0.1, bat_cap = 1, actual_load = "none", actual_gen = "none", purchase_price = [1,1,1,1,1,1,1,1,2,2,2,2] , episode_len = 8760,num_preds = 24,render_mode = "none", load_shedding = "none"):

        super(EMSv0_3, self).__init__()

        #define time frame
        self.current_step = 0
        self.final_step = int(episode_len)-num_preds-2 #one years worth of steps

        #Might make a function for these
        #fill all of the actual loads NB!!! is just random for now NB!!! is normalised 0-1
        if isinstance(actual_load,str) :
            self.actual_load = np.random.rand(self.final_step+num_preds+1).astype(np.float32) #will load from a file or something
        else:
            self.actual_load = actual_load[:episode_len]
    
        #fill all of the actual generation steps.
        if isinstance(actual_gen,str):
            self.actual_gen  = np.random.rand(self.final_step+num_preds+1).astype(np.float32) #will load from file or something
        else:
            self.actual_gen  = actual_gen[:episode_len]

        #Fill the loadShedding indicator
        if isinstance(load_shedding,str):
            num_shedding   = np.random.randint(int(0.02*episode_len), int(0.05*episode_len))
            load_shed      = np.array([1]*num_shedding + [0]*(episode_len - num_shedding))
            np.random.shuffle(load_shed)
            self.load_shed = load_shed
        else:
            self.load_shed = load_shedding[:episode_len]

        #define vars for render
        self.off_peak_purchases = 0
        self.peak_purchases     = 0
        self.standard_purchases = 0
        self.unmet_load_total   = 0
        self.frames = []

        #Define a var for unmet load no that there is loadshedding
        self.unmet_load = 0

        #define the purchase price for every step of the year
        purchase_price = np.array(purchase_price).astype(np.float32)
        repetitions    = (self.final_step+num_preds+1) // len(purchase_price)
        remainder      = (self.final_step+num_preds+1) % len(purchase_price)
        self.purchase_price =np.concatenate([purchase_price]*repetitions+[purchase_price[:remainder]])#need to read in from somewhere

        #define var for storing the excess gen
        self.excess_gen = 0
        #define a var for determine amount purchased per step (dont want to make it total as this will incure growing penalties for the Agent if used in reward structure)
        self.step_purchased = 0
        #define the battery max capacity
        self.bat_cap = bat_cap
        #define the battery low threshold
        self.bat_threshold = np.float32(bat_threshold)
        #define default action
        self.default_action = 0
        #define actions and observations space
        n_actions = 2 # keeping it simple

        self.num_preds = num_preds # day ahead predictions
        self.action_space = spaces.Discrete(n_actions)
        # Dict space to store all the different things
        self.observation_space = spaces.Dict({
                "power_bal_forecast": gym.spaces.Box(low=-np.inf, high=np.inf, shape=(1,num_preds), dtype=np.float32),
                "price_forecast": gym.spaces.Box(low=0, high=np.inf, shape=(1,num_preds+1), dtype=np.float32),
                "island_forecast": gym.spaces.Box(low=0, high=1, shape=(1,num_preds+1), dtype=np.float32),
                "bat_level": gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),
                "current_power_bal": gym.spaces.Box(low=-np.inf, high=np.inf, shape=(1,), dtype=np.float32),
                })

    def step(self, action):

        #update the current state with the action (needs to be done before current_step is inc since we want to apply the action to the previous step to get the current state)
        self.update_state(action)
        #Calculate reward from the action
        reward = self.calc_reward()

        #inc time step into Future
        self.current_step += 1
        #get next observation (for next time step)
        observation = self.get_obs()
        #Set terminated to False since there are no failure states
        self.terminated = False
        #Check if timelimit reached
        self.truncated = False if self.current_step<self.final_step else True
        #dont know what to put into info for now
        info = {}
        return observation, reward, self.terminated, self.truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed = seed, options=options)

        self.current_step = 0
        self.terminated = False
        self.truncated = False

        #reset the state
        self.battery_level = self.bat_cap/2
        self.excess_gen = 0
        self.step_purchased = 0
        self.unmet_load = 0
        self.off_peak_purchases = 0
        self.peak_purchases     = 0
        self.standard_purchases = 0
        self.unmet_load_total   = 0
        #get the first observation
        observation = self.get_obs()
        #Still don't know what to do with info
        info = {}
        return observation, info

    def render(self, mode='human', save_path=None):

        plt.clf()
        values = [self.off_peak_purchases, self.standard_purchases, self.purchase_price[self.peak_purchases]]
        colors = ['green', 'orange','red']
        labels = ['Off Peak', 'Standard', 'Peak']
        plt.xlim(0,1.6)
        plt.ylim(0,100)
        plt.bar(list(range(3)),values, color=colors, tick_label=labels)
        self.frames.append(plt.gcf().canvas.tostring_rgb())
        plt.pause(0.000001)

  
    def close(self):
        #don't think i need this for my application
        pass

    def update_state(self, action):
        #Update current state with actions
        if action == 0: #do nothing action
            self.standby()
        elif action == 1: #buy from Grid
            self.purchase()
        else:  #error case
            raise ValueError(
                f"Received invalid action = {action} which is not part of the action space."
            )
        #case list for each action?

    def calc_reward(self):
        #Calculate reward based on the state
        reward = -self.step_purchased*self.purchase_price[self.current_step] - self.unmet_load*10

        return reward

    def get_obs(self):
        #Fill the observation space with the next observation

        #Get Forecasts Will probaly write a function for this? idk maybe a schlep to return all the info
        load_forecast  = np.array( [self.actual_load[self.current_step+1: self.current_step + self.num_preds+1]] , dtype = np.float32) #will load from a file or something
        if load_forecast.shape != (1,self.num_preds):
            print(f"load_forecast shape is {load_forecast.shape} but it should be {(1, self.num_preds)}. Current step is {self.current_step}")
        gen_forecast   = np.array( [self.actual_gen[self.current_step+1: self.current_step + self.num_preds+1]] , dtype = np.float32) #will load from a file or something
        if gen_forecast.shape != (1,self.num_preds):
            print(f"gen_forecast shape is {gen_forecast.shape} but it should be {(1, self.num_preds)}. Current step is {self.current_step}")
        #calculate the power forecast
        power_bal_forecast = gen_forecast-load_forecast
        #get the prices for the current frame and the next 24 hours. Maybe will cut this down since that seems like a lot of info
        price_forecast = np.array( [self.purchase_price[self.current_step:self.current_step+self.num_preds+1]] , dtype = np.float32)
        #Just for readibility of the dict object
        bat_level      = np.array([self.battery_level] , dtype= np.float32)
        #island forecasst, same as tou forecast
        island_forecast =np.array( [self.load_shed[self.current_step:self.current_step+self.num_preds+1]] , dtype = np.float32)

        #calculate the current power balance
        current_load   = np.array([self.actual_load[self.current_step]], dtype = np.float32)
        current_gen    = np.array([self.actual_gen[self.current_step]], dtype  = np.float32)
        current_power_bal = current_gen - current_load



        obs = dict({
                "bat_level":      bat_level,
                "current_power_bal" :   current_power_bal,
                "island_forecast": island_forecast,
                "power_bal_forecast":  power_bal_forecast,
                "price_forecast": price_forecast,
        })
        return obs

    def standby(self):
        #ems stands by, load is met by generation, battery and then grid
        #if there is excess generation it is used to charge the batteries

        #define step_gen and step_load for readability
        step_gen  =  self.actual_gen[self.current_step]
        step_load =  self.actual_load[self.current_step]
        battery   =  self.battery_level
        islanded  =  self.load_shed[self.current_step]
        #reset purchased and unmet load amount
        self.step_purchased = 0
        #should have had step indicated in the name.
        self.unmet_load     = 0

        #check for gen meeting load
        if step_load <= step_gen :
            #Purchased electricity stays at 0 since there is sufficient generation.        
            #calulate the excess elec that was generated
            step_excess = step_gen - step_load
            #check if battery needs to be charged
            if battery < self.bat_cap :
                #check if the excess amount that was generated is less than the available capacity
                if self.bat_cap-battery-step_excess > 0:
                    self.battery_level += step_excess
                else:
                    #if the excess is greater than the availability then charge till full
                    self.battery_level = self.bat_cap
                    #set step excess to excess minus the amount used to charge
                    step_excess -= (self.bat_cap-battery)
                    self.excess_gen += step_excess
            else:
                #if the battery is full then just inc excess_gen
                self.excess_gen += step_excess
        else:
            #if the generation does not meet load
            step_shortfall = step_load - step_gen
            #checking if battery is above a threshold.
            if battery > self.bat_threshold:
                #check if battery has enough capacity to meet the load
                if battery - step_shortfall >= self.bat_threshold:
                    #if it does then subtract the shortfall from battery level
                    self.battery_level -= step_shortfall
                    #Purchased electricity stays at 0 since there is sufficient generation.     
                    
                else:
                    #set the battery to min value and purchase the rest from the grid
                    self.battery_level = self.bat_threshold
                    #calculate how much needs to be purchased
                    step_shortfall -= (battery - self.bat_threshold)
                    #check if the microgrid is grid connected
                    if islanded:
                        #if it is then set the unmet load to the shortfall
                        self.unmet_load = step_shortfall
                    else:
                        #if it is grid connected, purchase the shortfall.
                        self.step_purchased = step_shortfall
            else:
                #no battery available, therefore everything needs to be bought from the grid.
                if islanded:
                    #if it is then set the unmet load to the shortfall
                    self.unmet_load = step_shortfall
                else:
                    #if it is grid connected, purchase the shortfall.
                    self.step_purchased = step_shortfall
                    if self.purchase_price[self.current_step] == 1:
                        self.off_peak_purchases += 1

                    elif self.purchase_price[self.current_step] == 2:
                        self.standard_purchases += 1
                    else:
                        self.peak_purchases += 1


    def purchase(self):
        #purchase electricity to charge battery even if there is enough generation (I assume this will be used to buy at lower prices)
        #get values for readability
        step_load = self.actual_load[self.current_step]
        step_gen  = self.actual_gen[self.current_step]
        battery = self.battery_level
        islanded = self.load_shed[self.current_step]

        #Check if it is possible to buy electricity
        if islanded:
            #if its not then impliment the standby mode which handles load shedding
            self.standby()
        else:
            #if there is no loadshedding then proceed with purchase as normal
            #calculate the total power need (the load plus the amount that the battery needs to charge)
            total_need = step_load + (self.bat_cap-battery)
            #if the generation is less than the need then purchase the remainder
            if step_gen<total_need:
                #purchashing the shortfall
                self.step_purchased = total_need - step_gen
                #inc the purchase count
                if self.purchase_price[self.current_step] == 1:
                    self.off_peak_purchases += 1
                elif self.purchase_price[self.current_step] == 2:
                    self.standard_purchases += 1
                else:
                    self.peak_purchases += 1                
                #setting the battery levels to full
                self.battery_level = self.bat_cap
            else:
                #if the gen is enough then set purchase to 0
                self.step_purchased  = 0
                #set the battery to fully charged
                self.battery_level = self.bat_cap
                #inc excess_gen by caluclating the excess between the step gen and the total need (includes amount needed to charge the battery)
                self.excess_gen += (step_gen - total_need)


print("Current working directory: " + os.getcwd())

path_data = ".\EEE4022S_BNKJUL001_Thesis\PythonWorkspace\dataClean.csv"
data = pd.read_csv(path_data)

path_gen = ".\EEE4022S_BNKJUL001_Thesis\Generation\BNKJUL001_Thesis_solarGen500kWHomer.csv"
data_gen = pd.read_csv(path_gen)

#Not actually using this rn but will be soon :)
path_shedding = ".\EEE4022S_BNKJUL001_Thesis\MatlabWorkSpace\loadShedding2022.csv"
data_shedding = pd.read_csv(path_shedding)
load_shedding = data_shedding['LoadShedding'].values.astype(np.float32)

actual_gen = data_gen['PV_Out'].values.astype(np.float32)
actual_load = data['AC'].values.astype(np.float32)
purchase_price = data['tou_id'].values.astype(np.float32)


base_env = EMSv0_3(episode_len = 100, actual_load = actual_load, actual_gen = actual_gen, bat_threshold = 100, bat_cap = 500, purchase_price = purchase_price,num_preds = 3)
obs,_    = base_env.reset()
score = 0
obs,_    = base_env.reset()
#ensure that the exit condition is reset
truncated = False
#define the action to take
action_standby = 0

while not truncated:
    obs,reward,terminated,truncated,info = base_env.step(action_standby)
    score += reward
    base_env.render()
print(f"Done iteration! Total reward accumulated is: {score}")