import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt


#Plots a gaph of rates vs fills for a given channel

#Arguments
# sys.argv[1] = channel number
channel = str(int(sys.argv[1])) 

#fill_array = [8474, 8675, 8685, 8686, 8690, 8692, 8701, 8723, 8724, 8739]
#fill_array = [8474, 8484, 8489, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]
#fill_array = [8474, 8484, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]

#fill_array = [8063, 8067, 8072, 8073, 8076, 8102, 8136, 8151, 8178, 8210, 8220, 8260, 8304, 8314, 8331, 8385, 8402, 8474, 8675, 8685, 8686, 8690, 8692, 8701, 8723, 8724, 8739, 8773, 8782, 8817, 8858, 8873,8895, 8896,9020, 9031, 9032,9036, 9057, 9063, 9066]
#fill_array=[8773, 8782, 8817, 8873, 8895, 8896, 9031, 9036, 9057, 9063]
fill_array = [8063, 8067, 8072, 8073, 8076, 8102, 8136, 8151, 8178, 8210, 8220, 8260, 8304, 8314, 8331, 8385, 8402, 8474, 8724, 8739, 8773, 8782, 8817, 8858, 8873,8895, 8896,9020, 9031, 9032,9036, 9057, 9063, 9066]

eb_num = 1
new_albedo_array = []
ratio_array_old = []
ratio_array_new = []


# Read data from CSV file
csv_file_path = '/localdata/lgeneros/data_ch_'+str(channel)+'_1.csv'
data = pd.read_csv(csv_file_path)

# Specify the columns for the scatter plot
fill_column = "fill"
y1_column = "old_ratio"
y2_column = "new_ratio"

data = data[['fill', 'old_ratio', 'new_ratio']]

x_array = [i for i in range(1, len(fill_array) + 1)]
y1_array = data[y1_column]
y2_array = data[y2_column]
#fill_array = data[fill_column]
    
print(x_array)
print(y1_array)
print(y2_array)


#PLOT
fig = plt.figure()
fig.set_figheight(5.5)
#plt.subplots_adjust(wspace=0, hspace=0)

custom_yticks = [-2.5,-2.0,-1.5,-1.0, -0.5, -0.25, 0, 0.25, 0.5, 1.0, 1.5, 2.0, 2.5]

plt.title('Relative ratios vs Fills - Channel '+str(channel), fontsize=18)

#plt.text(16,1.5, "Channel "+ str(int(channel)), fontsize= 12, color = "darkorange", fontweight = "bold")
plt.scatter(x_array, y1_array, label='old albedo', color= 'dodgerblue', marker= "o", s=10)
plt.scatter(x_array, y2_array, label='new albedo', color="darkorange", marker='o', s=10)


plt.xticks(x_array, fill_array, rotation=80, fontsize = 8)
plt.xlim(-1,len(fill_array)+1)

plt.yscale('symlog')
plt.yticks(custom_yticks, custom_yticks, fontsize = 10)
plt.ylim(-5.5,5.5)    

#plt.xticklabels(custom_xtick_labels)
#plt.yticks(custom_yticks)
#plt.yticklabels(custom_ytick_labels)

plt.xlabel('Fill Number')
plt.ylabel('First empty bunch ratio %')

xcoords = [1, 5, 9, 11, 15, 19, 24, 29]
# colors for the lines
date = ['07/22','08/22','09/22','10/22','11/22','05/23','06/23','07/23']

for xc, d in zip(xcoords,date):
    plt.axvline(x=xc -0.3, color="grey", linestyle = 'dashed', linewidth = 0.5)
    plt.text(xc + 0.05, 0.9, d, rotation=90, color='grey', va='center', fontsize = 9)

#plt.axvspan(19-0.3, 25+0.3, alpha=0.3, color='lightblue', label = 'low threshold')

plt.legend(loc='upper right')

plt.savefig('ratio_fill_channel_'+channel+'_new.pdf')
