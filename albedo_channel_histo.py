import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt
import math


#Plots a gaph of the new correction vs fills for each channel

#Arguments
# sys.argv[1] = channel number

fill_array = [8724,8739,8773,8782,8817,8858,8873,8895,8896,9031,9036,9057,9063,9066]

channel_array = np.arange(48)
colors = ['dodgerblue', 'green', 'darkorange', 'purple', 'cyan', 'magenta', 'gray', 'pink','navy', 'blue', 'lime', 'gold', 'olive','red']
eb_num = 1
new_albedo_array = []
ratio_array_old = []
ratio_array_new = []




#HISTO PLOT
fig = plt.figure()
plt.figure(figsize=(10, 6))
plt.title('New albedo correction channel distribution - filtered', fontsize=15)
hist_range = (0, 1.5)


i=0
mean_array = []
for fill in fill_array:
    # Read data from CSV file
    csv_file_path = '/localdata/lgeneros/data_fill_'+str(fill)+'.csv'
    data = pd.read_csv(csv_file_path)

    data = data[['Channel', 'Ratio']]
    old_albedo = 2.2410375592529844

    # Specify the columns for the scatter plot
    
    filtered_data = data.dropna()
    x_array = filtered_data['Ratio'].tolist()
    
    x_array_red = []
    for x in x_array:
        x += old_albedo
        if x <= 0.6 and x>=0:
            x_array_red.append(x)
    #x_array_red = x_array
    print(x_array)
    print("Reduced "+ str(x_array_red))

    hist_values, bin_edges = np.histogram(x_array_red, bins='auto')
    
    
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Calculate the mean using the bin centers and heights
    mean = np.sum(bin_centers * hist_values) / np.sum(hist_values)
    mean_array.append(mean)
    print(mean_array)
    mean = round(mean, 2)
    
    
    plt.hist(x_array_red, bins=30, range=[0,1.5],edgecolor='black', alpha=0.5, label='Fill '+str(fill) + ' - mean: '+ str(mean),align='left', color=colors[i])
    
    i+=1


#average mean
data = np.array(mean_array)
ave_mean = sum(data)/len(data)
print("Average Mean: ", ave_mean)
#plt.xlim(-0.1,1.6) 
plt.xlim(-0.1,0.6)
plt.xticks(np.arange(0, 1.5, 0.1))
#plt.yticks(fontsize = 10)
#plt.ylim(-1.5,1.5)    


plt.xlabel('New Albedo')
#plt.ylabel('New albedo correction %')
plt.legend(loc='upper right')
plt.savefig('ratio_channel_histo.pdf')


