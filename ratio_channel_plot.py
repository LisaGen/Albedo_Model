import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt


#Plots a gaph of ratios vs fills for each channel

#Arguments
# sys.argv[1] = channel number
fill = sys.argv[1]


#fill_array = [8474, 8675, 8685, 8686, 8690, 8692, 8701, 8723, 8724, 8739]
#fill_array = [8474, 8484, 8489, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]
#fill_array = [8474, 8484, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]

#channel_array = all_channels = np.arange(48)

eb_num = 1
new_albedo_array = []
ratio_array_old = []
ratio_array_new = []


# Read data from CSV file
csv_file_path = '/localdata/lgeneros/data_fill_'+str(fill)+'.csv'
data = pd.read_csv(csv_file_path)

data = data[['channel', 'old_ratio']]
old_albedo = 2.2410375592529844

# Specify the columns for the scatter plot
x_array = []
y_array = []

for row in data.itertuples(index=False):
    channel = getattr(row, 'channel')
    old_ratio = getattr(row, 'old_ratio')

    # Check if old_ratio is empty
    if old_ratio:
        x_array.append(channel)
        y_array.append(old_ratio + old_albedo)
    else:
        x_array.append(channel)
        y_array.append(np.nan)  # Use numpy.nan for missing values

#fill_array = data[fill_column]
    
print(x_array)
print(y_array)


#PLOT
fig = plt.figure()
#plt.subplots_adjust(wspace=0, hspace=0)

custom_yticks = [-1.00,-0.75,-0.50,-0.25,0.00,0.25, 0.50,0.75,1.00]

plt.title('New albedo correction vs Channel - Fill  '+str(fill), fontsize=15)

#plt.text(16,1.5, "Channel "+ str(int(channel)), fontsize= 12, color = "darkorange", fontweight = "bold")
plt.scatter(x_array, y_array, color= 'dodgerblue', marker= "o", s=10)



plt.xticks(x_array, x_array, rotation=70,fontsize = 10)
plt.xlim(0,48)

#plt.yscale('symlog')
plt.yticks(custom_yticks, custom_yticks, fontsize = 10)
plt.ylim(-1.5,1.5)    


plt.xlabel('Channel Number')
plt.ylabel('New albedo correction %')

plt.savefig('ratio_channel_fill_'+fill+'.pdf')
