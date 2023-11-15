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

def parse_time(t):
    return datetime.strptime(t, '%H:%M:%S')

def format_time(dt):
    return dt.strftime('%H:%M')

def plot_in_line_fromCSV(filename, outpdf,axname='Time', col_names=['Channel 1 [hPascal]'], log_flag=False):

  df=pd.read_csv(filename, header=10,delimiter=';')
  pp=PdfPages(outpdf)
  print(df)
  print(df.keys())
 
  time=list()
  for t in df[axname]:
    hhmmss=parse_time(t)
    hhmm  =format_time(hhmmss)
    time.append(hhmm)
  print(time)

  for col_name in col_names:
    fig,ax=plt.subplots(figsize=(8,4.5))
    fig.autofmt_xdate(rotation=45)
    #ax.plot(range(len(df_cut)),df_cut[col_name])
    ax.plot(time,df[col_name], label=col_name)
    ax.set_ylabel(col_name)
    ax.set_xlabel(axname)
    ax.legend(ncol=2)
    #ax.set_xticks(rotation=45)
    #ax.set_xticks(ax.get_xticks(), rotation=45)
    print(ax.get_xticks())
    print(ax.get_xticklabels())
    #ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    if log_flag:
      ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
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
