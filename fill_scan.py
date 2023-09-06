import pandas as pd, pylab as py, numpy as np, tables as t
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

import sys

do_albedo_correction = sys.argv[1]
channel = sys.argv[2]
fillnum = sys.argv[3]

fills_non_corrected = []
fills_corrected = []


#folder_reprocessed = './23/8675_False/'
if sys.argv[4] == "new": #new processor dir
    folder_reprocessed = glob.glob("new_albedo_" +sys.argv[1]+"_"+str(sys.argv[2])+"_23/8675/")

elif sys.argv[4] == "old":  #old processor dir
    folder_reprocessed = glob.glob('Channel_'+str(channel)+'_23_old/'+str(fillnum)+'/')

else:
    print("Error")


print(folder_reprocessed)
for fill in folder_reprocessed:
    files = dir_list = os.listdir(str(fill))
    print(fill) 
    bxraw_reprocessed = []
    for file in files:
        print(file)
        h5 = t.open_file(fill+'/'+file)
        for row in h5.root.bcm1flumi.iterrows():
            bxraw_reprocessed.append(row['bxraw'])
        h5.close()

    bxraw_reprocessed_tot_orig_channel = [sum(x) for x in zip(*bxraw_reprocessed)]




fig,ax = py.subplots(facecolor='white')
py.step([x+1 for x in range(len(bxraw_reprocessed_tot_orig_channel))],bxraw_reprocessed_tot_orig_channel,where='mid', alpha = 0.8)
py.xlabel('BCID')
py.ylabel('bxraw summed')
#py.text(3000, 1000, str(fill), boxstyle ='round', facecolor = 'lightgray',edgecolor = 'black',linewidth= 1,pad= 0.5, horizontalalignment='center', verticalalignment='center', fontsize=12)

py.title('Total bxraw vs BCID')
py.savefig("fill_"+str(fillnum)+"_scan_"+str(channel)+".pdf")
