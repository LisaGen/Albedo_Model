#same as further_empty_bunches.py buth plots a single channel

#TFour arguments :
# sys.argv[1] = number of fill
# sys.argv[2] = number of the empty bunch that you want to analyze (first, second, ...)
# sys.argv[3] = old or new aledo correction
# sys.argv[4] = channel
              
import pandas as pd, pylab as py, numpy as np, tables as t
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

import sys

fill_num = sys.argv[1]
eb_num =  int(sys.argv[2])#number of the empty bunch that you want to analyze (first, second, ...)
channel = sys.argv[4]

all_xpoints = []
all_ypoints = []


print(channel)
do_albedo_correction = True
channel_mask = channel

fills_non_corrected = []
fills_corrected = []

if sys.argv[3] == "new": #new processor dir
    folder_reprocessed = glob.glob("Channel_"+str(channel)+"_23_new/"+str(fill_num)+"/")

elif sys.argv[3] == "old":  #old processor dir
    folder_reprocessed = glob.glob("Channel_"+str(channel)+"_23_old/"+str(fill_num)+"/")

else:
    print("Error")



print(folder_reprocessed)
for fill in folder_reprocessed:
    files = dir_list = os.listdir(str(fill))
    print("Fill" + fill) 
    bxraw_reprocessed = []
    for file in files:
        print("File" + file)
        h5 = t.open_file(fill+'/'+file)
        for row in h5.root.bcm1flumi.iterrows():
            bxraw_reprocessed.append(row['bxraw'])
        h5.close()

    bxraw_reprocessed_tot_orig_channel = [sum(x) for x in zip(*bxraw_reprocessed)]

#scanning all trains 

#trains = [200, 700, 1000, 1200, 1500, 2000, 3000] #for fill 8701
trains = [200, 300, 700, 1200, 1300, 1700, 2000, 2200, 2500, 2900, 3000]
x_length = len(trains)
ratios = []
for x in trains:
    print("Train" + str(x))
    a = 0
    for i in range(x,len(bxraw_reprocessed_tot_orig_channel)):
        if(bxraw_reprocessed_tot_orig_channel[i]>100 and bxraw_reprocessed_tot_orig_channel[i+1]<0.1*bxraw_reprocessed_tot_orig_channel[i]):
            a = i
            break

    bxraw_first_bunch = bxraw_reprocessed_tot_orig_channel [a-2:a+3]
    print(bxraw_reprocessed_tot_orig_channel[a-2:a+3])
    ratio = bxraw_reprocessed_tot_orig_channel[a+eb_num]/bxraw_reprocessed_tot_orig_channel[a]
    print(ratio)
    ratios.append(ratio*100)
    

print("Ratios:"+str(ratios))

#compute the average of the array  
total_sum = sum(ratios)
ave_ratio = total_sum / len(ratios)/100
print("Average ratio" ave_ratio)

#find a new albedo correction for the first empty bunch
old_albedo = 0.022410375592529844
new_albedo = ave_ratio + old_albedo
print("New first empty bunch correction" + str(new_albedo))

#plot ratios vs trains
fig = plt.figure()
plt.subplots_adjust(wspace=0, hspace=0)

custom_xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
custom_xtick_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

custom_yticks = [-10, -5, 0, 5, 10]
custom_ytick_labels = [-10, -5, 0, 5, 10]

plt.title('Counts Ratio vs Train Number - new albedo ', fontsize=18)

plt.text(6,-12, "Channel "+ str(channel), fontsize= 12, color = "darkorange", fontweight = "bold")
plt.scatter([1, 2, 3, 4, 5, 6, 7,8,9,10,11], ratios, color= "dodgerblue", marker= "o", s=10)

#for ax in fig.get_axes():

plt.xlim([0,12])
plt.ylim([-15,15])    

plt.xticks(custom_xticks)
#plt.xticklabels(custom_xtick_labels)
plt.yticks(custom_yticks)
#plt.yticklabels(custom_ytick_labels)

plt.xlabel('Train Number')
plt.ylabel('%')

if sys.argv[3] == "new":
   plt.savefig('ratio_trains_'+str(fill_num)+'_'+channel+'_new_albedo.pdf')
   
elif sys.argv[3] == "old":
   plt.savefig('ratio_trains_'+str(fill_num)+'_'+channel+'_old_albedo.pdf')
else:
   print("Error")
