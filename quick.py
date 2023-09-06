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

eb_num =  1 #number of the empty bunch that you want to analyze (first, second, ...)


csv_file_path = '/localdata/lgeneros/data_fill_'+str(fill)+'.csv'

if not os.path.exists(csv_file_path):
    # Create the CSV file if it doesn't exist
    with open(csv_file_path, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['Channel', 'Ratio'])

with open(csv_file_path, mode='a', newline='') as file:
    

    #good_ch = [3,4,5,6,7,8,10,11,12,13,14,15,17,18,19,20,21,22,26,27,28,29,30,31,32,33,34,35,36,37,44,45,46,47]
    good_ch = [3,4,5,6,7,8,10,11,12,13,14,15,17,18,19,20,21,22,26,27,28,29,30,31,32,33,34,35,36,37,44,45,46,47]
    for channel in good_ch:
        print ("Channel  " , str(channel))
        folder_reprocessed = glob.glob('Channel_'+str(channel)+'_'+str(year)+'_old/'+str(fill)+"/")

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

        #SCANNING LAST TRAIN

        bcid = len(bxraw_reprocessed_tot_orig_channel) - 1

        while bcid > 0 : 
            if bxraw_reprocessed_tot_orig_channel[bcid] > 100 and bxraw_reprocessed_tot_orig_channel[bcid+1]<0.1*bxraw_reprocessed_tot_orig_channel[bcid]:
                break
            else:
                bcid -= 1
        print('BCID: '+str(bcid))
        ratio = bxraw_reprocessed_tot_orig_channel[bcid+eb_num]/bxraw_reprocessed_tot_orig_channel[bcid]*100
        print(ratio)
        print("Ratios: "+ str(ratio))
        row = [channel, ratio]
        writer = csv.writer(file)
        writer.writerow(row)