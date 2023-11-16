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
from datetime import datetime

def common_suffix(strings):
  if not strings:
      return ""
  # Reverse the strings and find the common reversed suffix
  reversed_strings = [s[::-1] for s in strings]
  common_prefix_reversed = os.path.commonprefix(reversed_strings)
  # Revert the common suffix back to its original orientation and return
  return common_prefix_reversed[::-1]

def parse_datetime(t):
    return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

def parse_time(t):
    return datetime.strptime(t, '%H:%M:%S')

def format_time(dt):
    return dt.strftime('%H:%M')

def plot_in_line_fromCSV(filename, outpdf, col_names=['Channel 1 [hPascal]'], interval_tlabel=5, log_flag=False):

  df=pd.read_csv(filename, header=10,delimiter=';')
  pp=PdfPages(outpdf)
  print(df)
  print(df.keys())
 
  time_data=list()
  for d,t in zip(df['Date'],df['Time']):
    print(d,t)
    print(d+' '+t)
    dts=parse_datetime(d+' '+t)
    time_data.append(dts)
  print(time_data)
  df['DateTime']=time_data

  cut=df['DateTime']<datetime(2023,11,15,11,20)

  for col_name in col_names:
    fig,ax=plt.subplots(figsize=(8,4.5))
    #fig.autofmt_xdate(rotation=45)
    #ax.plot(time_data,df[col_name], label=col_name)
    ax.plot(df['DateTime'],df[col_name], label=col_name)
    ax.set_ylabel(col_name)
    ax.set_xlabel('Time')
    ax.legend(ncol=2)
    print(ax.get_xticks())
    print(ax.get_xticklabels())
    #ax.set_xticks(time_data[::interval_tlabel])
    #ax.set_xticklabels([t.strftime('%m/%d %H:%M') for t in time_data[::interval_tlabel]], rotation=45, ha='center')
    ax.set_xticks(df['DateTime'][::interval_tlabel])
    ax.set_xticklabels([t.strftime('%m/%d %H:%M') for t in df['DateTime'][::interval_tlabel]], rotation=45, ha='center')
    if log_flag:
      ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')

    ##cut1
    fig1,ax1=plt.subplots(figsize=(8,4.5))
    ax1.plot(df['DateTime'][cut],df[col_name][cut], label=col_name)
    ax1.set_ylabel(col_name)
    ax1.set_xlabel('Time')
    ax1.legend(ncol=2)
    time_data_cut=df['DateTime'][cut].copy()
    ax1.set_xticks(time_data_cut[::interval_tlabel])
    ax1.set_xticklabels([t.strftime('%m/%d %H:%M') for t in time_data_cut[::interval_tlabel]], rotation=45, ha='center')
    if log_flag:
      ax1.set_yscale('log')
    fig1.tight_layout()
    pp.savefig(fig1)
    plt.close('all')

  pp.close()

def plot_single_along_axis():
  datadir='../data/PKR/'
  filename='DATALOG_20231115_102905.csv'
  outpdf='example.pdf'
  fname=datadir+'*.csv'
  plot_in_line_fromCSV(datadir+filename,outpdf, log_flag=True)

if __name__=="__main__":

  plot_single_along_axis()
