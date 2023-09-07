import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt


#Plots a gaph of frist term of new_albedo vs channels for all fills in the chosen set

#Arguments
# sys.argv[1] = channel number
fill_array = [8724,8739,8773,8782,8817,8858,8873,8895,8896,9031,9036,9057,9063,9066]

channel_array = np.arange(48)
colors = ['dodgerblue', 'green', 'darkorange', 'purple', 'cyan', 'magenta', 'brown', 'gray', 'pink','red','dodgerblue', 'green', 'darkorange', 'purple','dodgerblue', 'green', 'darkorange', 'purple']
eb_num = 1
new_albedo_array = []
ratio_array_old = []
ratio_array_new = []

#SCATTER PLOT
fig = plt.figure()
plt.figure(figsize=(20, 9))
custom_yticks = [-1.00,-0.75,-0.50,-0.25,0.00,0.25, 0.50,0.75,1.00]
plt.title('New albedo correction vs Channel', fontsize=15)



i=0
for fill in fill_array:
    # Read data from CSV file
    csv_file_path = '/localdata/lgeneros/data_fill_'+str(fill)+'.csv'
    data = pd.read_csv(csv_file_path)

    data = data[['Channel', 'Ratio']]
    old_albedo = 2.2410375592529844

    # Specify the columns for the scatter plot
    x_array = []
    y_array = []
    
    for row in data.itertuples(index=False):
        channel = getattr(row, 'Channel')
        old_ratio = getattr(row, 'Ratio')

        # Check if old_ratio is empty
        if old_ratio:
            x_array.append(channel)
            y_array.append(old_ratio + old_albedo)
        else:
            x_array.append(channel)
            y_array.append(np.nan)  # Use numpy.nan for missing values

    #fill_array = data[fill_column]
    


    #plt.text(16,1.5, "Channel "+ str(int(channel)), fontsize= 12, color = "darkorange", fontweight = "bold")
    plt.scatter(np.array(x_array)+0.05*i, y_array, c= colors[i], marker= "o", s=15, label="Fill "+str(fill))
    i+=1


plt.xticks(x_array, x_array, rotation=70,fontsize = 10)
plt.xlim(0,48)

plt.yticks(custom_yticks, custom_yticks, fontsize = 10)
plt.ylim(-1.5,1.5)    


plt.xlabel('Channel Number')
plt.ylabel('New albedo correction %')
plt.legend(loc='lower right')

plt.savefig('ratio_channel_scatter.pdf')
