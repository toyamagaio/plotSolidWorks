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

  #cut=df['DateTime']<datetime(2023,11,17,12,30)
  cut1=df['DateTime']<datetime(2023,11,21,12,00) #just before kaiho
  cut2=df['DateTime']<datetime(2023,11,20,18,10) #before scroll stop
  cut3=(df['DateTime']>datetime(2023,11,20,18,15)) & (df['DateTime']<datetime(2023,11,21,12,00))#after scroll stop, before kaiho
  cuts=[cut1,cut2,cut3]

  cut1=df['DateTime']<datetime(2023,12,12,9,30) #
  cuts=[]

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
    ax.grid(color='0.5', linestyle='--', linewidth=0.5)
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')

    ##cut1
    for cut in cuts:
      fig1,ax1=plt.subplots(figsize=(8,4.5))
      ax1.plot(df['DateTime'][cut],df[col_name][cut], label=col_name)
      ax1.set_ylabel(col_name)
      ax1.set_xlabel('Time')
      ax1.legend(ncol=2)
      time_data_cut=df['DateTime'][cut].copy()
      npoint=len(time_data_cut)
      ax1.set_xticks(time_data_cut[::int(npoint/10)])
      ax1.set_xticklabels([t.strftime('%m/%d %H:%M') for t in time_data_cut[::int(npoint/10)]], rotation=45, ha='center')
      ax1.grid(color='0.5', linestyle='--', linewidth=0.5)
      if log_flag:
        ax1.set_yscale('log')
      fig1.tight_layout()
      pp.savefig(fig1)
      plt.close('all')

  pp.close()

def compare(filenames, labels, outpdf, col_name='Channel 1 [hPascal]', interval_tlabel=5, log_flag=False, max_hours=None):

  pp=PdfPages(outpdf)
  fig,ax=plt.subplots(figsize=(8,4.5))

  colors=['k','r']
  if len(filenames)>2:
    colors=[cmap(i) for i in range(len(filenames))]

  for i,(filename,label,color) in enumerate(zip(filenames,labels,colors)):
    df=pd.read_csv(filename, header=10,delimiter=';')
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
    df['TimeDelta']=[ t-time_data[0] for  t in time_data ]
    df['hours'] = [ t.total_seconds()/3600 for t in df['TimeDelta']]

    if max_hours != None:
      cut=(df['hours']<max_hours)
      ax.plot(df['hours'][cut],df[col_name][cut], label=label)
    else:
      ax.plot(df['hours'],df[col_name], label=label)

  
  ####
  #t=[0,7./60.,1.+34./60., 2.]
  #p=[48,4.62e-2,8.88e-3, 6.15e-3]
  #ax.scatter(t,p,color='k',marker='x',label='t=1.5 (stycast seal)')
  ####
  ax.set_ylabel(col_name)
  ax.set_xlabel('Time [h]')
  ax.legend(ncol=2)
  #print(ax.get_xticks())
  #print(ax.get_xticklabels())
  #ax.set_xticks(df['hours'][::interval_tlabel])
  #ax.set_xticklabels([t.strftime('%m/%d %H:%M') for t in df['DateTime'][::interval_tlabel]], rotation=45, ha='center')
  if log_flag:
    ax.set_yscale('log')
  ax.grid(color='0.5', linestyle='--', linewidth=0.5)
  fig.tight_layout()
  pp.savefig(fig)
  plt.close('all')

  pp.close()

def plot_single_along_axis():
  datadir='../data/PKR/'
  #filename='DATALOG_20231115_102905.csv'
  #outpdf='example.pdf'

  #filename='DATALOG_20231117_114333.csv' #11:44 scroll on +  11:51 TMP on 
  #outpdf='blank_20231117_genatsu.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  #filename='DATALOG_20231117_114333.csv' #11:44 scroll on +  11:51 TMP on 
  #outpdf='blank_20231117_genatsu.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  #filename='DATALOG_20231117_173411.csv' #TMP on 
  #outpdf='blank_20231117_TMP.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=False, interval_tlabel=240)

  #filename='DATALOG_20231120_104159.csv' #TMP off 
  #outpdf='blank_20231120_TMPoff.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=180)
  
  ###CFRP####
  #t=1.0 (1)
  #filename='DATALOG_20231211_164551.csv' #TMP on 
  #outpdf  ='t=1.0_20231211_TMPon.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=30)

  #filename='DATALOG_20231211_204712.csv' #TMP off
  #outpdf  ='t=1.0_20231211_TMPoff.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  #blank
  filename='DATALOG_20231212_103606.csv' #TMP on 
  outpdf  ='CFRP_blank_20231212_TMPon.pdf'
  plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  filename='DATALOG_20231212_143735.csv' #TMP off 
  outpdf  ='CFRP_blank_20231212_TMPoff.pdf'
  plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  #t=1.5
  #filename='DATALOG_20231212_185723.csv' #TMP on 
  #outpdf  ='CFRP_t1.5_20231212_TMPon.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

  #filename='DATALOG_20231212_230248.csv' #TMP off 
  #outpdf  ='CFRP_t1.5_20231212_TMPoff.pdf'
  #plot_in_line_fromCSV(datadir+filename,outpdf, col_names=['Channel 1 [Pascal]'],log_flag=True, interval_tlabel=60)

def plot_compare():
  datadir='../data/PKR/'
  ##CFRP vacuuming
  fnames=['DATALOG_20231212_103606.csv','DATALOG_20231213_190128.csv','DATALOG_20231211_164551.csv','DATALOG_20231212_185723.csv','DATALOG_20231219_115111.csv','DATALOG_20231220_092517.csv','DATALOG_20231220_144124.csv','DATALOG_20231222_202955.csv','DATALOG_20231224_142230.csv']
  labels   =['blank','blank(2)','t=1.0 mm', 't=1.5 mm','t=1.5 mm (w/ seal)','t=1.5 mm(2)','t=1.5 mm (w/ seal, 2)','t=1.5 mm (w/ seal, 3)','t=1.5 mm (seal both)']
  filenames=[datadir+fname for fname in fnames]
  ##outpdf='pdf/CFRP_vacuuming2.pdf'
  #outpdf='pdf/CFRP_vacuuming3_seal.pdf'
  #compare(filenames, labels, outpdf, col_name='Channel 1 [Pascal]', interval_tlabel=5, log_flag=True)
  outpdf='pdf/CFRP_vacuuming3_seal_5hours.pdf'
  compare(filenames, labels, outpdf, col_name='Channel 1 [Pascal]', interval_tlabel=5, log_flag=True, max_hours=5)

  ##CFRP sealing
  #fnames=['DATALOG_20231212_143735.csv','DATALOG_20231214_084107.csv','DATALOG_20231211_204712.csv','DATALOG_20231212_230248.csv','DATALOG_20231219_143838.csv','DATALOG_20231220_120855.csv','DATALOG_20231220_171345.csv','DATALOG_20231223_133000.csv','DATALOG_20231225_085709.csv']
  #labels   =['blank','blank(2)','t=1.0 mm', 't=1.5 mm','t=1.5 mm (w/ seal)','t=1.5 mm(2)','t=1.5 mm (w/ seal, 2)','t=1.5 mm (w/ seal, 3)','t=1.5 mm (seal both)']
  #filenames=[datadir+fname for fname in fnames]
  ##outpdf='pdf/CFRP_compare_TMPoff3_seal.pdf'
  ##compare(filenames, labels, outpdf, col_name='Channel 1 [Pascal]', interval_tlabel=5, log_flag=True)
  #outpdf='pdf/CFRP_compare_TMPoff3_seal_5hours.pdf'
  #compare(filenames, labels, outpdf, col_name='Channel 1 [Pascal]', interval_tlabel=5, log_flag=True, max_hours=5)

if __name__=="__main__":
  #plot_single_along_axis()
  plot_compare()
