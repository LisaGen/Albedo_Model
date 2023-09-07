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

#Proides relative rates (nth empty bunch/last full bunch)
#It takes rates from data that are processed with the old albedo, so the new albedo is given by new_albedo = relative_rate + old_albedo
#ARGUMENTS:
# sys.argv[1] = fill number

print ("Fill  " + sys.argv[1])

fill = int(sys.argv[1])


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

#NEW CORRECTION

eb_num =  3 #number of the empty bunch that you want to analyze (first, second, ...)
#old albedo to add 
old_alb_1 = 0.022410375592529844
old_alb_2 = 0.0023920368925298427
old_alb_3 = 0.0007854522325298428
#if you want to upudate further albdo terms, pleas remeber to add the corresponding old albedo and change it when the new albedo is defined

csv_file_path = '/localdata/lgeneros/data_fill_'+str(fill)+'_'+str(eb_num)+'.csv'

if not os.path.exists(csv_file_path):
    # Create the CSV file if it doesn't exist
    with open(csv_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Channel', 'Ratio', 'New Albedo'])

with open(csv_file_path, mode='a', newline='') as file:
    

    #good_ch = [3,4,5,6,7,8,10,11,12,13,14,15,17,18,19,20,21,22,26,27,28,29,30,31,32,33,34,35,36,37,44,45,46,47]
    good_ch = [3,4,5,6,7,8,14,15,17,18,19,20,21,22,26,27,28,29,30,31,32,33,34,35,36,37]
    for channel in good_ch:
        print ("Channel  " , str(channel))
        folder_reprocessed = glob.glob(str(fill)+'_const_old23/'+str(fill)+'/')

        print(folder_reprocessed)
        for fill_num in folder_reprocessed:
            files = dir_list = os.listdir(str(fill_num))
            print("Fill" + fill_num) 
            bxraw_reprocessed = []
            for file1 in files:
                print("File" + file1)
                h5 = t.open_file(fill_num+'/'+file1)
                for row in h5.root.bcm1flumi.iterrows():
                    bxraw_reprocessed.append(row['bxraw'])
                h5.close()

            bxraw_reprocessed_tot_orig_channel = [sum(x) for x in zip(*bxraw_reprocessed)]

        #SCAN of the LAST TRAIN

        bcid = len(bxraw_reprocessed_tot_orig_channel) - 1

        while bcid > 0 : 
            if bxraw_reprocessed_tot_orig_channel[bcid] > 100 and bxraw_reprocessed_tot_orig_channel[bcid+1]<0.1*bxraw_reprocessed_tot_orig_channel[bcid]:
                break
            else:
                bcid -= 1
        print('BCID: '+str(bcid))
        ratio = bxraw_reprocessed_tot_orig_channel[bcid+eb_num]/bxraw_reprocessed_tot_orig_channel[bcid]
        new_alb = ratio + old_alb_+str(eb_num) 
    
        print("Ratios: "+ str(ratio))
        print("New Albedo: "+ str(new_alb))
        row = [channel, ratio, new_alb]
        writer = csv.writer(file)
        writer.writerow(row)
        
