import tables as t, pylab as py, pandas as pd, os, queue as Queue, numpy as np
import sys
import shutil
import matplotlib.dates as mdates
from statistics import mean
from scipy.optimize import curve_fit
import os
import glob
import matplotlib.pyplot as plt


# Read data from CSV file
#csv_file_path = '/localdata/lgeneros/albedo_function.csv'
#data = pd.read_csv(csv_file_path)

# Specify the columns for the scatter plot
#x_column = "BCID"
#y_column = "Albedo_correction"


#data = data[["BCID", "Albedo_correction"]]
#x = data[x_column]
albedo_model_old = np.array([1.0, 0.022410375592529844, 0.0023920368925298427, 0.0007854522325298428])
albedo_tail = [0.00030464839252984286, 0.00022096663252984283, 0.00018857369252984284, 0.00017816717252984283, 0.00017519799252984283, 0.00017183887252984284, 0.00016958514252984284, 0.00016651578252984285, 0.00016273452252984284, 0.00016219435252984283, 0.00015808399252984284, 0.00015572652252984285, 0.00015465688252984283, 0.00015297554252984285, 0.00015145875252984284, 0.00014926227252984284]

print(len(albedo_tail))

x = np.arange(1, 21)
y = np.array([1.0])
y_old = np.concatenate((albedo_model_old, albedo_tail)) *100
print(len(y_old))

ave_1 = 0.005244808716170002
ave_2 = 0.0007509161683906839
ave_3 = 4.3792521392825125e-05




y = np.append(y,ave_1)
y = np.append(y,ave_2)
y = np.append(y,ave_3)

y = np.append(y,albedo_tail)

y = y*100


# Calculate the slope and intercept
print(y[4])
print(y[3])
print(y[2])

slope = (y[4] - y[2]) / (x[4] - x[2])
intercept = y[4] - slope * x[4]
third_correction = intercept + slope * x[3]
print('Third correction: ', third_correction)
third_correction_tr=float(f'{third_correction:.3f}')
# Generate x values for the line
x_line_fit = np.linspace(x[1], x[5], num=100)
y_line_fit = [slope * xi + intercept for xi in x_line_fit]

# Plot the scatter plot and the fitted line
plt.yscale('log')

plt.scatter(x+0.2, y_old, color='dodgerblue', label='Old Albedo')
plt.scatter(x, y, color='yellowgreen', label='New Albedo')
#plt.plot(x_line_fit, y_line_fit, color='orange', label='Interpolation Line')
plt.scatter(x[3], third_correction, color='yellowgreen', marker='o')
#plt.text(12,7,'Fitted third correction: '+str(third_correction_tr)+'%', fontsize=8, color='black', ha='left', va='center', weight='bold')


plt.xticks(np.arange(1, 21),np.arange(1, 21))
plt.ylim(0.01,200) 
plt.xlabel('BCID')
plt.ylabel('Albedo correction %')
plt.legend()
plt.title('Albedo Model')
#plt.grid(True)
plt.savefig('third_correction.pdf')

# Print the slope and intercept
print("Slope:", slope)
print("Intercept:", intercept)