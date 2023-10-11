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

eps=0.05

def calculate_distance_to_point(row, x, y, z):
    return np.sqrt((row['X [mm]'] - x) ** 2 + (row['Y [mm]'] - y) ** 2 + (row['Z [mm]'] - z) ** 2)
    #return np.sqrt((row['X [m]'] - x) ** 2 + (row['Y [m]'] - y) ** 2 + (row['Z [m]'] - z) ** 2) ##horiuchi data

def calculate_distance_to_axis(row, value1, value2, axis1, axis2):
    return np.sqrt((row[axis1] - value1)**2 + (row[axis2] - value2)**2)

def common_suffix(strings):
  if not strings:
      return ""
  # Reverse the strings and find the common reversed suffix
  reversed_strings = [s[::-1] for s in strings]
  common_prefix_reversed = os.path.commonprefix(reversed_strings)
  # Revert the common suffix back to its original orientation and return
  return common_prefix_reversed[::-1]

def plot_in_line(files, times, outpdf, outcsv, v1, v2, ax1='X [mm]',ax2='Y [mm]', col_names=['Density (Fluid) [kg/m^3]']):
  df0=pd.read_csv(files[0], delimiter='\t')
  print(df0.keys())
  #add distance columns to the data frame
  df0['Distance'] = df0.apply(lambda row: calculate_distance_to_axis(row, v1, v2, ax1,ax2), axis=1)
  df0['time']=float(times[0])
  df0= df0[pd.notna(df0['Pressure [Pa]'])]
  
  min_distance_idx = df0['Distance'].idxmin()
  print(min_distance_idx)

  ##print selected row information
  min_distance_row = df0.loc[min_distance_idx]
  print("closest distance row:")
  print(min_distance_row[['X [mm]', 'Y [mm]', 'Z [mm]']])
  print("distance:", min_distance_row['Distance'])
  print(min_distance_row)
  v1_cl, v2_cl=min_distance_row[[ax1, ax2]]
  print(ax1,v1_cl,ax2,v2_cl)
  cut_idx= (np.abs(df0[ax1]-v1_cl)<eps) & (np.abs(df0[ax2]-v2_cl)<eps) 
  df_cut=df0[cut_idx]
  print(len(df_cut))
  print(df_cut)

  print('cut_idx:{}'.format(cut_idx))

  ax3=['X [mm]', 'Y [mm]', 'Z [mm]']
  ax3.remove(ax1)
  ax3.remove(ax2)
  print(ax3)

  #cut_idx= (df0['Y [mm]']<100) & (df0['Y [mm]']>-100)

  pp=PdfPages(outpdf)
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(df0['X [mm]'][cut_idx],df0['Y [mm]'][cut_idx],df0['Z [mm]'][cut_idx])
  ax.set_xlabel('X [mm]')
  ax.set_ylabel('Y [mm]')
  ax.set_zlabel('Z [mm]')
  #ax.set_xlim(-5, 5)
  #plt.show()
  pp.savefig(fig)

  print(df_cut.index)
  cut_idx_list=df_cut.index
  print(cut_idx_list)

  #for col_name in col_names:
  #  fig,ax=plt.subplots(figsize=(8,4.5))
  #  #ax.plot(range(len(df_cut)),df_cut[col_name])
  #  ax.plot(df_cut[ax3[0]],df_cut[col_name])
  #  ax.set_ylabel(col_name)
  #  #ax.set_yscale('log')
  #  fig.tight_layout()
  #  pp.savefig(fig)
  #  plt.close('all')
  #pp.close()

  df=pd.DataFrame()

  for file, time in zip(files, times):
    print(file,time)
    df_a = pd.read_csv(file, delimiter='\t', header=0, skiprows=lambda x: x != 0 and (x not in cut_idx_list+1))
    df_a['Distance']=df_a.apply(lambda row: calculate_distance_to_axis(row, v1, v2, ax1, ax2), axis=1)
    df_a['time']=float(time)
    print(df_a)
    df=pd.concat([df,df_a])
    #break

  ftimes=[float(t) for t in times]
  ftimes.sort()

  for col_name in col_names:
    fig,ax=plt.subplots(figsize=(8,4.5))
    #ax.plot(range(len(df_cut)),df_cut[col_name])
    for time in ftimes:
      ax.plot(df[df['time']==time][ax3[0]],df[df['time']==time][col_name], label='t={:.2f} us'.format(time*1e6))
    ax.set_ylabel(col_name)
    ax.legend(ncol=3)
    #ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')
  pp.close()
  
  df.to_csv(outcsv,index=False)


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
  #print(min_distance_row[['X [m]', 'Y [m]', 'Z [m]']])
  print("distance:", min_distance_row['Distance'])
  print(min_distance_row)
  x_cl, y_cl, z_cl=min_distance_row[['X [mm]', 'Y [mm]', 'Z [mm]']]
  #x_cl, y_cl, z_cl=min_distance_row[['X [m]', 'Y [m]', 'Z [m]']]

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
    ax.set_yscale('log')
    fig.tight_layout()
    pp.savefig(fig)
    plt.close('all')
  pp.close()

  ##output csv
  df.to_csv(outcsv,index=False)

def read_example():
  datadir='../data/example/'
  #datadir='../data/No.3 (1000Pa, 5MPa-1000Pa)/'
  #datadir='../data/No.4 (100Pa, 5MPa-1000Pa)/'
  #datadir='../data/No.8 (1Pa, 5MPa-1000Pa)/' #good
  #datadir='../data/No.7 (10Pa, 5MPa-1000Pa)/' #good
  #datadir='../data/_No.11 (100kPa, 5MPa-1000Pa)/' #good
  #datadir='../data/_No.10 (10000Pa, 5MPa-10000Pa)/' #good
  #datadir='../data/_No.9 (1Pa, 5MPa-100Pa)/' #good
  #datadir='../data/test_from_horiuchi/'
  #datadir='../data/No.5_single1000Pa_5MPa-1000Pa/'

  outdir='../pdf/'
  outcsvdir='../csv/'
  outpdf='example.pdf'
  outcsv='example.csv'
  #outpdf='horiuchi.pdf'
  #outcsv='horiuchi.csv'
  #outpdf=outdir+'horiuchi.pdf'
  #outcsv=outcsvdir+'horiuchi.csv'
  #outpdf=outdir   +'No5.pdf'
  #outcsv=outcsvdir+'No5.csv'
  fname=datadir+'*.txt'
  files=glob.glob(fname)
  print(files)
  times_tmp=files
  prefix = os.path.commonprefix(times_tmp)
  suffix = common_suffix(times_tmp)
  times = ['0.'+label[len(prefix):-len(suffix)] for label in times_tmp]
  print(times)
  print(len(times))
  x,y,z=0,0,0
  #x,y,z=0,0.6,0.6
  #plot_at_point(files,times,outpdf,outcsv,x,y,z,col_names=['Density (Fluid) [kg/m^3]', 'Pressure [Pa]', 'Temperature [K]'])
  print('ouputpdf: {}'.format(outpdf))

  v1=y
  v2=z
  plot_in_line(files, times, outpdf, outcsv, v1, v2, ax1='Y [mm]',ax2='Z [mm]', col_names=['Density (Fluid) [kg/m^3]','Pressure [Pa]', 'X [mm]','Y [mm]', 'Z [mm]','Distance'])


def read_all():
  mother_dir='../data/'
  dirs=glob.glob(mother_dir+'_No*/')
  outdir='../pdf/'
  ids=[dire[len(mother_dir):len(mother_dir)+5].replace(' ','') for dire in dirs]
  print(dirs,ids)
  return

  for datadir,ide in zip(dirs,ids):
    outpdf=outdir+ide+'_example.pdf'
    outcsv='../csv/'+ide+'_example.csv'
    fname=datadir+'*.txt'
    files=glob.glob(fname)
    print(files)
    labels_tmp=files
    prefix = os.path.commonprefix(labels_tmp)
    suffix = common_suffix(labels_tmp)
    labels = ['0.'+label[len(prefix):-len(suffix)] for label in labels_tmp]
    print(labels)
    print(len(labels))
    #x,y,z=0,0,0
    x,y,z=0,0,0
    plot_at_point(files,labels,outpdf,outcsv,x,y,z,col_names=['Density (Fluid) [kg/m^3]', 'Pressure [Pa]', 'Temperature [K]'])
    print('ouputpdf: {}'.format(outpdf))

if __name__=="__main__":
  read_example()
  #read_all()
