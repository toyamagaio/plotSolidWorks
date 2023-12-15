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

def plot_in_line_fromCSV(filenames, labels, outpdf, log_flag=False):
  unit_conversionRange = {
    'm' : 1e9,  #
    'cm': 1e7,  # 
    'mm': 1e6,  #
    'um': 1e3,  #
    'nm': 1.0,  #
    'A' : 0.1,  #
  }
  unit_conversionEne = {
    'eV' : 1,  #
    'keV': 1e3,  # 
    'MeV': 1e6,  #
  }


  pp=PdfPages(outpdf)
  fig, ax=plt.subplots()
  for filename, label in zip(filenames,labels):
    df=pd.read_csv(filename)
    #print(df)
    print(df.keys())
    for index, row in df.iterrows():
      unitE = row['unitE']  #
      unitR = row['unitRange']  #
      if unitR in unit_conversionRange:
        conversion_factor = unit_conversionRange[unitR]
        df.at[index, 'Range'] *= conversion_factor
      if unitE in unit_conversionEne:
        conversion_factor = unit_conversionEne[unitE]
        df.at[index, 'Energy'] *= conversion_factor
 
    cut=df['Energy']<1000
    ax.plot(df['Energy'][cut],df['Range'][cut], label=label)
    ax.set_ylabel('Range [nm]')
    ax.set_xlabel('Energy [eV]')
    ax.legend(ncol=2)
    ax.grid(color='0.5', linestyle='--', linewidth=0.5)
    if log_flag:
      ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')

  pp.close()

def plot_single_along_axis():
  datadir='../../'

  filenames=['SRIM_muHe4inSilver.csv' ,'SRIM_muHe4inAl.csv'] 
  labels =['Ag' ,'Al'] 
  outpdf='SRIM_muHe4inAgAl_cut.pdf'
  f_list=[datadir+fname for fname in filenames]
  plot_in_line_fromCSV(f_list,labels,outpdf,log_flag=False)

if __name__=="__main__":

  plot_single_along_axis()
