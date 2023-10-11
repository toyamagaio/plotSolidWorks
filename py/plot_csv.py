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

def common_suffix(strings):
  if not strings:
      return ""
  # Reverse the strings and find the common reversed suffix
  reversed_strings = [s[::-1] for s in strings]
  common_prefix_reversed = os.path.commonprefix(reversed_strings)
  # Revert the common suffix back to its original orientation and return
  return common_prefix_reversed[::-1]

def compare(files,labels,outpdf,colnames=['Pressure [Pa]'], log_flag=False):
  outdir='../pdf/'
  colors=['k','r']
  if len(files)>2: colors=[cmap(i) for i in range(len(files))]

  df_list=list()

  for file in files:
    df=pd.read_csv(file)
    df_list.append(df)

  pp=PdfPages(outdir+outpdf)
  for colname in colnames:
    fig,ax=plt.subplots(figsize=(8,4.5))
    for df, label, color in zip(df_list, labels, colors):
      ax.plot(df['time'],df[colname],color=color,label=label,marker='o')
    ax.set_xlabel('time [sec]')
    ax.set_ylabel(colname)
    if log_flag:
      ax.set_yscale('log')
    ax.legend()
    fig.tight_layout()
    pp.savefig(fig)
  pp.close()

def plot_in_line_fromCSV(filename, ftimes, outpdf,axname='X [mm]', col_names=['Density (Fluid) [kg/m^3]'], log_flag=False):

  df=pd.read_csv(filename)
  pp=PdfPages(outpdf)

  for col_name in col_names:
    fig,ax=plt.subplots(figsize=(8,4.5))
    #ax.plot(range(len(df_cut)),df_cut[col_name])
    for time in ftimes:
      ax.plot(df[df['time']==time][axname],df[df['time']==time][col_name], label='t={:.2f} us'.format(time*1e6))
    ax.set_ylabel(col_name)
    ax.set_xlabel(axname)
    ax.legend(ncol=2)
    if log_flag:
      ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')
  pp.close()

def compare_horisetup():
  files =['../csv/horiuchi.csv','../csv/hori1.csv']
  labels=['by Koba','by Hori']
  outpdf='comp_hori.pdf'
  compare(files,labels,outpdf,colnames=[ 'Temperature [K]', 'Density (Fluid) [kg/m^3]', 'Pressure [Pa]'])
  outpdf='comp_hori_log.pdf'
  compare(files,labels,outpdf,colnames=[ 'Temperature [K]', 'Density (Fluid) [kg/m^3]', 'Pressure [Pa]'], log_flag=True)

def plot_single():
  files =['../csv/horiuchi.csv']
  labels=['by Koba']
  outpdf='hori_log.pdf'
  compare(files,labels,outpdf,colnames=[ 'Temperature [K]', 'Density (Fluid) [kg/m^3]', 'Pressure [Pa]','Mach Number [ ]'])

def plot_single_along_axis():
  datadir='../data/example/'
  filename='example.csv'
  outpdf='example_ax.pdf'
  fname=datadir+'*.txt'
  files=glob.glob(fname)
  print(files)
  times_tmp=files
  prefix = os.path.commonprefix(times_tmp)
  suffix = common_suffix(times_tmp)
  times = ['0.'+label[len(prefix):-len(suffix)] for label in times_tmp]
  ftimes=[float(t) for t in times]
  ftimes.sort()
  print(ftimes)
  ftimes_dec=[ ftimes[i] for i in range(0,len(ftimes),3)]
  print(ftimes_dec) 
  plot_in_line_fromCSV(filename,ftimes_dec,outpdf,axname='X [mm]', col_names=['Density (Fluid) [kg/m^3]','Pressure [Pa]', 'Temperature [K]', 'X [mm]','Y [mm]', 'Z [mm]','Distance'])

if __name__=="__main__":

  compare_horisetup()
  plot_single()
  plot_single_along_axis()
  plot_single()
