#Prints 48 plots in 4 pages (cp = compact plots) of the ratio between the nth empty bunch and the last full bunch
#Three arguments :
# sys.argv[1] = number of fill
# sys.argv[2] = number of the empty bunch that you want to analyze (first, second, ...)
# sys.argv[3] = old or new aledo correction

              
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

all_xpoints = []
all_ypoints = []

for channel in range(1,49):
    print(channel)
    do_albedo_correction = True
    channel_mask = channel

    fills_non_corrected = []
    fills_corrected = []

    if sys.argv[3] == "new": #new processor dir
        folder_reprocessed = glob.glob("Channel_"+str(channel)+"_22_new/"+str(fill_num)+"/")
                                       
    elif sys.argv[3] == "old":  #old processor dir
        folder_reprocessed = glob.glob("Channel_"+str(channel)+"_22_old/"+str(fill_num)+"/")

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
    #trains = [200, 300, 700, 1200, 1300, 1700, 2000, 2200, 2500, 2900, 3000]
    #trains = [600, 1500, 2300]
    #trains = [200, 600, 1200, 1500, 2000, 3000]
    #trains = [200, 600, 1200, 1600, 2200, 2500, 3000]
    #trains = [1000, 1500, 2000, 2500, 2800]
    trains =  [500, 1500, 2200, 3200]
    
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
    print("Ratios"+ str(ratios))

#plot ratios vs trains

    xpoints = np.arange(1, x_length +1)
    #xpoints = [1,3,5,7,9,11]
    ypoints = ratios

    all_xpoints.append(xpoints)
    all_ypoints.append(ypoints)
print("X ARRAY *******" + str(all_xpoints))
print("Y ARRAY *******" + str(all_ypoints))

#  Plots 

num_pages = 4
graphs_per_page = 12

for page in range(num_pages):
    fig = plt.figure()
    fig, ax = plt.subplots(3, 4)
    plt.subplots_adjust(wspace=0, hspace=0)
    fig.suptitle('First empty bunch Ratio vs Train - '+str(fill_num), fontsize=16)
    
    
    custom_xticks =  [1,2,3,4] #np.arange(1, x_length +1)
    custom_xtick_labels = [1,2,3,4] #np.arange(1, x_length +1)

    custom_yticks = [-10,-5, 0, 5, 10]
    custom_ytick_labels = custom_yticks
    
    for i in range(graphs_per_page):
        #Calculate the index of the current graph related to a channel
        channel = page * graphs_per_page + i
        
        if channel >= 12:  # Stop if all graphs have been plotted
            break

        ax = fig.add_subplot(4, 6, i+1)
        ax.text(1,-8, "Channel "+ str(channel+1), fontsize= 6, color = "darkorange", fontweight = "bold")
        ax.scatter(all_xpoints[channel], all_ypoints[channel], color= "dodgerblue", marker= "o", s=10)

    for ax in fig.get_axes():

        ax.set_xlim([0,x_length +1])
        ax.set_ylim([-15,15])    
    
        ax.set_xticks(custom_xticks)
        ax.set_xticklabels(custom_xtick_labels)
        ax.set_yticks(custom_yticks)
        ax.set_yticklabels(custom_ytick_labels)
    
        ax.set_xlabel('Train')
        ax.set_ylabel('%')
        ax.label_outer()
    py.savefig('rate_train_'+str(fill_num)+ '_pg'+str(page+1)+'.pdf')

