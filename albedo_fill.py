
import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt


all_xpoints = []
all_ypoints = []

g = 0
for channel in range(1 + g, 7 + g):

    #Calculates the new albedo corrections for all the fills in the array
    #Plots a gaph of new_albedo vs fills for each channel

    #Arguments
    # sys.argv[1] = channel number


    fill_array = [8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728]#, 8729, 8730, 8731, 8736, 8738, 8739 ]

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
        
        folder_reprocessed = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_old/'+str(fill)+"/")

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
        

        #find a new albedo correction for the first empty bunch
        old_albedo = 0.022410375592529844
        new_albedo = ave_ratio #+ old_albedo
        #print("New first empty bunch correction" + str(new_albedo))
        
        new_albedo_array.append(new_albedo)
    
        #plot ratios vs trains

        xpoints = [i for i in range(1, len(fill_array) + 1)] 
        #xpoints = [1,3,5,7,9,11]
        ypoints = new_albedo_array

    all_xpoints.append(xpoints)
    all_ypoints.append(ypoints)
print("X ARRAY *******" + str(all_xpoints))
print("Y ARRAY *******" + str(all_ypoints))

#  Plots 

num_pages = 1
graphs_per_page = 6

for page in range(num_pages):
    fig = plt.figure()
    fig, ax = plt.subplots(2, 3)
    plt.subplots_adjust(wspace=0.1, hspace=0.1)
    #fig.suptitle('New Albedo Corrections vs Fills', fontsize=16)
    fig.suptitle('Average ratio vs Fills', fontsize=16)
    
    
    for i in range(graphs_per_page):
        #Calculate the index of the current graph related to a channel
        channel = page * graphs_per_page + i
        
        if channel >= 6:  # Stop if all graphs have been plotted
            break

        ax = fig.add_subplot(2, 3, i+1)
        ax.text(16,-0.75, "Channel "+ str(channel + g), fontsize= 6, color = "darkorange", fontweight = "bold")
        ax.scatter(all_xpoints[channel], all_ypoints[channel], color= "dodgerblue", marker= "o", s=10)

    for ax in fig.get_axes():

        ax.set_xlim([0,x_length +2])
        ax.set_ylim([-1,1])    
    
        ax.set_xticks([i for i in range(1, len(fill_array) + 1)])
        ax.set_xticklabels(fill_array)
        ax.tick_params(axis='x', labelsize=3)
        ax.set_yticks([-0.50, -0.25, 0, 0.25, 0.50])
        ax.set_yticklabels([-0.50, -0.25, 0, 0.25, 0.50])
        ax.tick_params(axis='y', labelsize=5)
    
        ax.set_xlabel('Fills')
        ax.set_ylabel('ave_ratio')
        ax.label_outer()
    #py.savefig('new_albedo_fill_pg'+str(page+1)+'.pdf')
    py.savefig('ratio_fill_pg'+str(page+1)+'.pdf')
    
        
    