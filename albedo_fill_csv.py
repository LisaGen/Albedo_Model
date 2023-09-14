import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt
import csv

#Calculates the new albedo corrections for all the fills in the array
#Generates a CSV to plot a gaph of the first term of the new_albedo vs fills for a given channel

#Arguments
# sys.argv[1] = channel number
channel = sys.argv[1]


fill_array=[8773, 8782, 8817, 8873, 8895, 8896, 9031, 9036, 9057, 9063] #choose a set of fills


eb_num = 1 #first empty bunch (you can edit if you want subsequent albedo terms)

new_albedo_array = []
ratio_array_old = []
ratio_array_new = []

#new_rows = [['fill', 'old ratio', 'new ratio']]
new_rows = []


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
     
      #--------------------------OLD------------------------
         
    folder_reprocessed_old = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_old/'+str(fill)+"/")
   
    print(folder_reprocessed_old)
    for fill_num in folder_reprocessed_old:
        files = dir_list = os.listdir(str(fill_num))
        print("Fill" + fill_num) 
        bxraw_reprocessed_old = []
        for file in files:
            print("File" + file)
            h5 = t.open_file(fill_num+'/'+file)
            for row in h5.root.bcm1flumi.iterrows():
                bxraw_reprocessed_old.append(row['bxraw'])
            h5.close()

        bxraw_reprocessed_tot_orig_channel_old = [sum(x) for x in zip(*bxraw_reprocessed_old)]

    bcid_old = len(bxraw_reprocessed_tot_orig_channel_old) - 1

    while bcid_old > 0 : 
        if bxraw_reprocessed_tot_orig_channel_old[bcid_old] > 100 and bxraw_reprocessed_tot_orig_channel_old[bcid_old+1]<0.1*bxraw_reprocessed_tot_orig_channel_old[bcid_old]:
            break
        else:
            bcid_old -= 1
    print('BCID: '+str(bcid_old))
    ratio_old = bxraw_reprocessed_tot_orig_channel_old[bcid_old+eb_num]/bxraw_reprocessed_tot_orig_channel_old[bcid_old]*100
    #print('Old ratio % : '+ str(ratio_old))
    #ratio_array_old.append(ratio_old)
    
    
    #--------------------------NEW------------------------
    

    folder_reprocessed_new = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_new/'+str(fill)+"/")
   
    print(folder_reprocessed_new)
    for fill_num in folder_reprocessed_new:
        files = dir_list = os.listdir(str(fill_num))
        print("Fill" + fill_num) 
        bxraw_reprocessed_new = []
        for file in files:
            print("File" + file)
            h5 = t.open_file(fill_num+'/'+file)
            for row in h5.root.bcm1flumi.iterrows():
                bxraw_reprocessed_new.append(row['bxraw'])
            h5.close()

        bxraw_reprocessed_tot_orig_channel_new = [sum(x) for x in zip(*bxraw_reprocessed_new)]


    bcid_new = len(bxraw_reprocessed_tot_orig_channel_new) - 1

    while bcid_new > 0 : 
        if bxraw_reprocessed_tot_orig_channel_new[bcid_new] > 100 and bxraw_reprocessed_tot_orig_channel_new[bcid_new+1]<0.1*bxraw_reprocessed_tot_orig_channel_new[bcid_new]:
            break
        else:
            bcid_new -= 1
    print('BCID: '+str(bcid_new))
    ratio_new = bxraw_reprocessed_tot_orig_channel_new[bcid_new+eb_num]/bxraw_reprocessed_tot_orig_channel_new[bcid_new]*100
    #print('New ratio % : '+ str(ratio_new))
    #ratio_array_new.append(ratio_new)
    
    row = [fill, ratio_old, ratio_new]
    new_rows.append(row)
    
    # CSV file path
csv_file_path = '/localdata/lgeneros/data_ch_'+str(channel)+'.csv'

# Append new rows to the CSV file
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    for row in new_rows:
        writer.writerow(row)
