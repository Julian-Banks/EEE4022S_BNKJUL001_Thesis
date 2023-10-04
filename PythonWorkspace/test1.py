# load data clean for me 
#How do I add packages to the PATH



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# 1.1 load data
def load_data(path):
    data = pd.read_csv(path)
    return data
#Load the csv file called dataCleaned.csv into a dataframe called data
data = load_data('d:/UCT/4th year!/4022/EEE4022S_BNKJUL001_Thesis/PythonWorkspace/dataClean.csv')

#print an overview of the data
print(data.head())
print(data.describe())


#plot a histogram  of the AC variable
plt.hist(data.AC)
plt.xlabel('AC')
plt.ylabel('count')
plt.title('Histogram of AC')
plt.show()

#Break the DC variable down into its different modes
#plot a histogram of the DC variable
plt.hist(data.DC)
plt.xlabel('DC')
plt.ylabel('count')
plt.title('Histogram of DC')
plt.show()
#plot a histogram of the DC variable for each mode

