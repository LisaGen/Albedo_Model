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

#Calculates the new albedo corrections for all the channels in the array
#Plots a gaph of new_albedo vs fills for each channel

#Arguments
# sys.argv[1] = channel number
fill = int(sys.argv[1])


#fill_array = [8474, 8484, 8489, 8491, 8496, 8654, 8675, 8685, 8686, 8690, 8691, 8692, 8695, 8696, 8701, 8723, 8724, 8725, 8728, 8729, 8730, 8731, 8736, 8738, 8739]
#fill_array = [8063, 8067, 8072, 8073, 8076, 8102, 8136, 8151, 8178, 8210, 8220, 8260, 8304, 8314, 8331, 8385, 8402, 8474, 8675, 8685, 8686, 8690, 8692, 8701, 8723, 8724, 8739, 8858, 8895, 9020, 9032, 9066, 9073]
#fill_array = [8474, 8675, 8685, 8686, 8690, 8692, 8701, 8723, 8724, 8739]
#fill_array = [8063, 8067, 8072, 8073, 8076, 8102, 8136, 8151, 8178, 8210, 8220, 8260, 8304, 8314, 8331, 8385, 8402, 8858, 8895, 9020, 9032, 9066, 9073] #8265,
#fill_array = [8028,8030,8036,8773, 8782, 8817, 8822, 8873, 8895, 8896, 9031, 9036, 9042, 9057, 9063]
#fill_array = [8822]
ch_array=[3,4,5,6,7,8,14,15,17,18,19,20,21,22,26,27,28,29,30,31,32,33,34,35,36,37]


eb_num = 1

new_albedo_array = []
ratio_array_old = []
ratio_array_new = []

#new_rows = [['fill', 'old ratio', 'new ratio']]
new_rows = []

  
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
     
     
#row = [Channel,New Albedo]
for channel in ch_array:
             
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
    ratio = bxraw_reprocessed_tot_orig_channel_old[bcid_old+eb_num]/bxraw_reprocessed_tot_orig_channel_old[bcid_old]
    #print('Old ratio % : '+ str(ratio_old))
    #ratio_array_old.append(ratio_old)
    old_albedo = 0.022410375592529844
    new_albedo = ratio +old_albedo
    row = [channel,new_albedo]
        
    new_rows.append(row)
    
    # CSV file path
csv_file_path = '/localdata/lgeneros/data'+str(fill)+'_cbc_new.csv'

# Append new rows to the CSV file
with open(csv_file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    for row in new_rows:
        writer.writerow(row)
        print('appended')
