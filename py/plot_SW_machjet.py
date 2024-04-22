import sys
import os
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use('Agg')
import csv
import glob
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
cmap=plt.get_cmap('tab10')
from mpl_toolkits.mplot3d import Axes3D

def compare_alongZ(files,labels,outpdf,outcsv=None):
  fig, ax=plt.subplots(2,1,sharex='all')
  fig1, ax1=plt.subplots()
  df_out=pd.DataFrame()

  for i,(filename,label) in enumerate(zip(files,labels)):
    df=pd.read_csv(filename,delimiter='\t')
    df['filename']=filename
    df['label']=label
    yc=0
    zc=0
    dy=0.01
    dz=0.01
    cut=(df['Z [mm]']>zc-zd) & (df['Z [mm]']<zc+dz)&(df['Y [mm]']>yc-dy)&(df['Y [mm]']<yc+dy) &(df['Pressure [Pa]']>0)
    #cut=(df['Z [mm]']==0)&(df['Y [mm]']<0.1) &(df['Pressure [Pa]']>0)
    ax[0].plot(df[cut]['X [mm]'],df[cut]['Pressure [Pa]'],label=label)
    ax[1].plot(df[cut]['X [mm]'],df[cut]['Pressure [Pa]'],label=label)
    ax1.hist(df[cut]['Y [mm]'],label=label, alpha=0.5)
    df_out=pd.concat([df_out,df[cut]],axis=0,ignore_index=True)
  ax[1].set_xlabel('X [mm]')
  ax[0].set_ylabel('P [Pa]')
  ax[0].legend()
  ax[1].set_ylabel('P [Pa]')
  ax[1].set_yscale('log')
  ax1.legend()
  ax1.set_xlabel('Y [mm]')
  pp=PdfPages(outpdf)
  pp.savefig(fig)
  pp.savefig(fig1)
  pp.close()
  print('{} is saved.'.format(outpdf))

  if outcsv!=None:
    df_out.to_csv(outcsv)
    print('{} is saved.'.format(outcsv))
##########
def plot_a_file_alongZ(filename,outpdf,stepy=1.0, dy=0.2):
  df=pd.read_csv(filename,delimiter='\t')
  print(df.keys())
  '''Index(['X [mm]', 'Y [mm]', 'Z [mm]', 'Volume [m^3]', 'Surface [m^2]', 'Pressure [Pa]', 'Unnamed: 6'], dtype='object')'''
  cut=(df['Z [mm]']==0)&(df['Y [mm]']<0.1) &(df['Pressure [Pa]']>0)
  print(df[cut])
  Ymin=min(df[cut]['Y [mm]'])
  print('Ymin at Z=0: {}'.format(Ymin))
  cut2=(df['Z [mm]']==0)&(df['Y [mm]']>Ymin+0.5)&(df['Y [mm]']<0.7) &(df['Pressure [Pa]']>0)
  Ymin2=min(df[cut2]['Y [mm]'])
  print('Ymin2 at Z=0: {}'.format(Ymin2))
  
  
  fig, ax=plt.subplots(2,1,sharex='all')
  fig1, ax1=plt.subplots()
  ax[0].plot(df[cut]['X [mm]'],df[cut]['Pressure [Pa]'],label='Y={}'.format(Ymin))
  
  ax[1].plot(df[cut]['X [mm]'],df[cut]['Pressure [Pa]'])
  ax1.hist(df[cut]['Y [mm]'])
  
  Ymin_a=Ymin
  for i in range(5):
    print('Ymin_a=',Ymin_a)
    cut_a=(df['Z [mm]']==0)&(df['Y [mm]']>Ymin_a+stepy)&(df['Y [mm]']<Ymin_a+stepy+dy) &(df['Pressure [Pa]']>0)
    if len(df[cut_a]['Y [mm]'])>0:
      Ymin_a=min(df[cut_a]['Y [mm]'])
      ax[0].plot(df[cut_a]['X [mm]'],df[cut_a]['Pressure [Pa]'],label='Y={}'.format(Ymin_a))
      ax[1].plot(df[cut_a]['X [mm]'],df[cut_a]['Pressure [Pa]'])
      ax1.hist(df[cut_a]['Y [mm]'])
    else:
      print('beak',i)
      break
  
  
  ax[1].set_xlabel('X [mm]')
  ax[0].set_ylabel('P [Pa]')
  ax[0].legend()
  ax[1].set_ylabel('P [Pa]')
  ax[1].set_yscale('log')
  
  #plt.show()
  pp=PdfPages(outpdf)
  pp.savefig(fig)
  pp.savefig(fig1)
  pp.close()


if __name__=="__main__":
  
  #filename='../data/XZ_0.txt'
  #outpdf='../pdf/test.pdf'
  #plot_a_file_alongZ(filename,outpdf)

  files=['../data/No.8 (1Pa, 5MPa-1000Pa)/0928(1Pa, 5MPa-1000Pa)_0.txt', '../data/No.8 (1Pa, 5MPa-1000Pa)/0928(1Pa, 5MPa-1000Pa)_0.0000166.txt']
  labels=['(1) t=0','(2) t=0.0000166']
  outpdf='../pdf/test_compare.pdf'
  outcsv='../data/test.csv'
  compare_alongZ(files,labels,outpdf,outcsv=outcsv)
  #compare_alongZ(files,labels,outpdf)
