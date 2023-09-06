
import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt

#Calculates the new albedo corrections for all the fills in the array
#Plots a gaph of new_albedo vs fills for each channel

#Arguments
# sys.argv[1] = channel number
channel = str(int(sys.argv[1]) +1) #channel "i" in the hd5 files correspond to channel "i-1" in the list


fill_array = [8474, 8484, 8489, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]

eb_num = 1
new_albedo_array = []

for fill in fill_array:
    
    if fill<5633:
	    raise ValueError('Fill number too small, this script only works with 2017 and 2018 data')
    elif fill<6540:
	    year = 17
    elif fill<7920:
	    year = 18
    elif fill<8533:
	    year = 22
    else:
	    year = 23
     
    
    if fill in [8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]:
        
        folder_reprocessed = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_old/'+str(fill)+"/")
        
    elif fill in [8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723]:
        
        folder_reprocessed = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_new/'+str(fill)+"/")
    else:
        print("Error")
        
    
    print(folder_reprocessed)
    for fill_num in folder_reprocessed:
        files = dir_list = os.listdir(str(fill_num))
        print("Fill" + fill_num) 
        bxraw_reprocessed = []
        for file in files:
            print("File" + file)
            h5 = t.open_file(fill_num+'/'+file)
            for row in h5.root.bcm1flumi.iterrows():
                bxraw_reprocessed.append(row['bxraw'])
            h5.close()

        bxraw_reprocessed_tot_orig_channel = [sum(x) for x in zip(*bxraw_reprocessed)]


    #SCANNING ALL TRAINS 
    #Different arrays of trains depending on te fill profile
    
        
    if fill in [8675, 8685]:  #group A
        print("Group A")
        trains=[200, 300, 700, 1200, 1300, 1700, 2000, 2200, 2500, 2900, 3000]    
    elif fill in [8686, 8690, 8691, 8692, 8723]: #group B
        print("Group B")
        trains = [600, 1500, 2300]
    elif fill in [8695]: #group C
        print("Group C")
        trains = [200, 600, 1200, 1600, 2200, 2500, 3000]
    elif fill in [8696, 8701, 8724, 8725]: #group D
        print("Group D")
        trains = [200, 600, 1200, 1500, 2000, 3000]  
    elif fill in [8654]: #group E
        print("Group E")
        trains = [1000, 1500, 2000, 2500, 2800]
    elif fill in [8728, 8729, 8730]: #group F
        print("Group D")
        trains = [200, 600, 1200, 1500, 2000, 2550, 3000]
    elif fill in  [8731, 8736, 8738, 8739]: #group G
        trains = [1300, 2100, 3000] 
    else:
        print("Error")
                         
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
        #print(ratio)
        ratios.append(ratio*100)
    print("Ratios"+ str(ratios))

    #compute the average of the array  
    total_sum = sum(ratios)
    ave_ratio = total_sum / len(ratios)/100
    #print(ave_ratio)

    #find a new albedo correction for the first empty bunch
    old_albedo = 0.022410375592529844
    new_albedo = ave_ratio*100 #+ old_albedo
    #print("New first empty bunch correction" + str(new_albedo))
    
    new_albedo_array.append(new_albedo)
    
print(fill_array)
print(new_albedo_array)
#PLOT
fig = plt.figure()
#plt.subplots_adjust(wspace=0, hspace=0)

custom_yticks = [-2.5,-1.5, -0.5, 0, 0.5, 1.5, 2.5]
custom_ytick_labels = custom_yticks
#plt.xticks(x, custom_ytick_labels, fontsize=6)

plt.title('Average ratios vs Fills - new albedo', fontsize=18)

plt.text(14,2, "Channel "+ str(int(channel)-1), fontsize= 12, color = "darkorange", fontweight = "bold")
plt.scatter([i for i in range(1, len(fill_array) + 1)], new_albedo_array, color= "dodgerblue", marker= "o", s=10)

#for ax in fig.get_axes():

plt.xticks([i for i in range(1, len(fill_array) + 1)], fill_array, fontsize = 6)


plt.xlim(0,len(fill_array)+1)
plt.ylim(-3,3)    

#plt.xticklabels(custom_xtick_labels)
plt.yticks(custom_yticks)
#plt.yticklabels(custom_ytick_labels)

plt.xlabel('Fill Number')
plt.ylabel('ave_ratio %')


plt.savefig('ratio_fill_channel_'+channel+'_new.pdf')