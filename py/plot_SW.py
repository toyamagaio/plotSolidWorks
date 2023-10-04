import sys
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import csv
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
cmap=plt.get_cmap('tab10')

def calculate_distance_to_point(row, x, y, z):
    return np.sqrt((row['X [mm]'] - x) ** 2 + (row['Y [mm]'] - y) ** 2 + (row['Z [mm]'] - z) ** 2)

def calculate_distance_to_axis(row, value, axis='X [mm]'):
    return np.abs(row[axis] - value)

def common_suffix(strings):
  if not strings:
      return ""
  # Reverse the strings and find the common reversed suffix
  reversed_strings = [s[::-1] for s in strings]
  common_prefix_reversed = os.path.commonprefix(reversed_strings)
  # Revert the common suffix back to its original orientation and return
  return common_prefix_reversed[::-1]

def plot_at_point(files, times, outpdf, outcsv, x, y, z, col_names=['Density (Fluid) [kg/m^3]']):

  df0=pd.read_csv(files[0], delimiter='\t')
  print(df0.keys())
  #add distance columns to the data frame
  df0['Distance'] = df0.apply(lambda row: calculate_distance_to_point(row, x, y, z), axis=1)
  df0['time']=float(times[0])
  
  min_distance_idx = df0['Distance'].idxmin()

  ##print selected row information
  min_distance_row = df0.loc[min_distance_idx]
  print("closest distance row:")
  print(min_distance_row[['X [mm]', 'Y [mm]', 'Z [mm]']])
  print("distance:", min_distance_row['Distance'])
  print(min_distance_row)
  x_cl, y_cl, z_cl=min_distance_row[['X [mm]', 'Y [mm]', 'Z [mm]']]

  df=pd.DataFrame()

  for file, time in zip(files, times):
    print(file,time)
    df_a = pd.read_csv(file, delimiter='\t', header=0, skiprows=lambda x: x != 0 and x != min_distance_idx-1)
    df_a['Distance']=df_a.apply(lambda row: calculate_distance_to_point(row, x, y, z), axis=1)
    df_a['time']=float(time)
    #print(df_a)
    df=pd.concat([df,df_a])

  df=df.sort_values('time')
  print(df)

  ##plot figure
  pp=PdfPages(outpdf)
  for col_name in col_names:
    fig,ax=plt.subplots(figsize=(8,4.5))
    ax.plot(df['time'],df[col_name])
    ax.set_title('(X,Y,Z)=({0:.3f},{1:.3f},{2:.3f}) [mm]'.format(x_cl,y_cl,x_cl))
    ax.set_xlabel('time')
    ax.set_ylabel(col_name)
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')
  pp.close()

  ##output csv
  df.to_csv(outcsv,index=False)

def read_example():
  datadir='../data/example/'
  outdir='../pdf/'
  outpdf='example.pdf'
  outcsv='example.csv'
  fname=datadir+'*.txt'
  files=glob.glob(fname)
  print(files)
  labels_tmp=files
  prefix = os.path.commonprefix(labels_tmp)
  suffix = common_suffix(labels_tmp)
  labels = ['0.'+label[len(prefix):-len(suffix)] for label in labels_tmp]
  print(labels)
  print(len(labels))
  #plot_weight_spectra_raw(files, labels, outpdf, col_name='rawIntensity')
  plot_at_point(files,labels,outpdf,outcsv,0,0,0)
  print('ouputpdf: {}'.format(outpdf))

if __name__=="__main__":
  read_example()

