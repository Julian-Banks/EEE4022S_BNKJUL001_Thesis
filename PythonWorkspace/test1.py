# load data clean for me 
#How do I add packages to the PATH

import pandas as pd



# 1.1 load data
def load_data(path):
    data = pd.read_csv(path)
    return data
#Load the csv file called dataCleaned.csv into a dataframe called data
data = load_data('dataCleaned.csv')
