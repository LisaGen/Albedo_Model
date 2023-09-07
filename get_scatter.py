import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt

# Read data from CSV file
csv_file_path = '/localdata/lgeneros/albedo_function.csv'
data = pd.read_csv(csv_file_path)

# Specify the columns for the scatter plot
x_column = "BCID"
y_column = "Albedo_correction"


#data = data[["BCID", "Albedo_correction"]]
x = data[x_column]
y = data[y_column]*100


#PLOT
fig = plt.figure()

plt.title('Albedo Model')

#plt.text(16,1.5, "Channel "+ str(int(channel)), fontsize= 12, color = "darkorange", fontweight = "bold")
plt.scatter(x, y, label='old albedo', color= 'dodgerblue', marker= "o", s=10)


plt.xticks(np.arange(1, 21),np.arange(1, 21))  # Set x-axis ticks to integer values from 1 to 20
#custom_tick_labels = np.arange(1, 21)  # Using the same values as the ticks
#plt.gca().set_xticklabels(custom_tick_labels)
#plt.xticks(x_array, fill_array, rotation=80, fontsize = 8)
#plt.xlim(-1,len(fill_array)+1)

plt.yscale('log')
#plt.yticks(custom_yticks, custom_yticks, fontsize = 10)
plt.ylim(0.01,200)    

#plt.xticklabels(custom_xtick_labels)
#plt.yticks(custom_yticks)
#plt.yticklabels(custom_ytick_labels)

plt.xlabel('BCID')
plt.ylabel('Albedo correction %')


#plt.legend(loc='upper right')

plt.savefig('albedo_function.pdf')

