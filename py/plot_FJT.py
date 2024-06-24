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

def d_to_e_converter(value):
    return float(value.replace('D', 'E'))

def plot_XYZ(filename,names,Ncase=0,outcsvname='../data/delivery20240529/summary.csv'):
  fig_dir='../fig/FJTplots'
  if not os.path.isdir(fig_dir):
    os.makedirs(fig_dir)

  df=pd.read_csv(filename,delimiter='\s+',skiprows=3,header=None,names=names,converters={col: d_to_e_converter for col in names})
  print(df)
  x_min=min(df['X'])
  x_max=max(df['X'])
  y_min=min(df['Y'])
  y_max=max(df['Y'])
  z_min=min(df['Z'])
  z_max=max(df['Z'])
  ay_min=min(abs(df['Y']))
  az_min=min(abs(df['Z']))

  print('X: {0} -- {1}'.format(x_min,x_max))
  print('Y: {0} -- {1} absmin:{2}'.format(y_min,y_max,ay_min))
  print('Z: {0} -- {1} absmin:{2}'.format(z_min,z_max,az_min))

  eps=8e-4
  cut=(abs(df['Y'])<=ay_min+eps) & (abs(df['Z'])<=az_min+eps) & (df['Y']>0) & (df['Z']>0)
  cutX0=(df['X']==0) & (df['PRE']>0) #& (df['Z']==az_min)
  cutPRE=(df['PRE']>0)

  uniXs=np.unique(df['X'])
  uniYs=np.unique(df['Y'][cutPRE])
  uniZs=np.unique(df['Z'][cutPRE])
  print(uniXs)
  print(uniYs)
  print(uniZs)

  print('df[cut]',df[cut])
  idx_max=df['X'][cut].idxmax()
  print(idx_max)

  cut_uniq= (cut) & (df.index<=idx_max)
  cut_uniq2= (cut_uniq) & (df['X']>=0.1)

  df['case']=np.full(len(df),Ncase)

  #if os.path.isfile(outcsvname):
  #  df[cut_uniq].to_csv(outcsvname,mode='a',index=False,header=None)
  #else:
  #  df[cut_uniq].to_csv(outcsvname,index=False)

  #npX =list()
  #npXP=list()
  #for uniX in uniXs:
  #  cutX =(df['X']==uniX)
  #  cutXP=(df['X']==uniX) & (df['PRE']>0)
  #  print('X',uniX,'len',len(df['X'][cutX]))

  #fig1,ax1=plt.subplots(figsize=(10,5))
  #fig2,ax2=plt.subplots(figsize=(10,5))
  #fig3,ax3=plt.subplots(figsize=(10,5))
  #fig4,ax4=plt.subplots(figsize=(10,5))
  #fig5,ax5=plt.subplots(figsize=(10,5))
  #fig6,ax6=plt.subplots(figsize=(10,5))
  #x_margin=0.025

  #ax1.plot(df['X'][cut_uniq],df['PRE'][cut_uniq],color='b')
  #ax1.set_title('Pressure')
  #ax1.set_xlabel('X [m]')
  #ax1.set_ylabel('P [Pa]')
  #ax1.set_yscale('log')
  #ax1.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax1.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax1.axvline(0,alpha=0.5,color='r')
  #ax1.axvline(x_max,alpha=0.5,color='r')
  #ax1.axvline(0.1265,alpha=0.5,color='g')
  #fig1.tight_layout()

  #ax2.plot(df['X'][cut_uniq],df['N(/cm^3)'][cut_uniq],color='k')
  #ax2.set_title('Num. of density')
  #ax2.set_xlabel('X [m]')
  #ax2.set_ylabel('N [/cm^3]')
  #ax2.set_yscale('log')
  #ax2.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax2.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax2.axvline(0,alpha=0.5,color='r')
  #ax2.axvline(x_max,alpha=0.5,color='r')
  #ax2.axvline(0.1265,alpha=0.5,color='g')
  #fig2.tight_layout()

  #ax3.plot(df['X'][cut_uniq],df['Mach'][cut_uniq],color='m')
  #ax3.set_title('r=sqrt(Y^2+Z^2)')
  #ax3.set_xlabel('X [m]')
  #ax3.set_ylabel('Mach')
  #ax2.set_yscale('log')
  #ax3.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax3.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax3.axvline(0,alpha=0.5,color='r')
  #ax3.axvline(x_max,alpha=0.5,color='r')
  #ax3.axvline(0.1265,alpha=0.5,color='g')
  #fig3.tight_layout()

  #ax4.plot(df['X'][cut_uniq],np.sqrt(df['Y'][cut_uniq]**2+df['Z'][cut_uniq]**2),color='orange')
  #ax4.set_title('r=sqrt(Y^2+Z^2)')
  #ax4.set_xlabel('X [m]')
  #ax4.set_ylabel('r [m]')
  #ax4.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax4.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax4.axvline(0,alpha=0.5,color='r')
  #ax4.axvline(x_max,alpha=0.5,color='r')
  #ax4.axvline(0.1265,alpha=0.5,color='g')
  #fig4.tight_layout()

  #ax5.plot(df['X'][cut_uniq2],df['PRE'][cut_uniq2],color='b')
  #ax5.set_title('Pressure')
  #ax5.set_xlabel('X [m]')
  #ax5.set_ylabel('P [Pa]')
  #ax5.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax5.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax5.axvline(0,alpha=0.5,color='r')
  #ax5.axvline(x_max,alpha=0.5,color='r')
  #ax5.axvline(0.1265,alpha=0.5,color='g')
  #fig5.tight_layout()

  #ax6.plot(df['X'][cut_uniq2],df['N(/cm^3)'][cut_uniq2],color='k')
  #ax6.set_title('Num. of density')
  #ax6.set_xlabel('X [m]')
  #ax6.set_ylabel('N [/cm^3]')
  #ax6.set_yscale('log')
  #ax6.set_xlim(x_min-x_margin,x_max+x_margin)
  #ax6.grid(color='0.5', linestyle='--', linewidth=0.5)
  #ax6.axvline(0,alpha=0.5,color='r')
  #ax6.axvline(x_max,alpha=0.5,color='r')
  #ax6.axvline(0.1265,alpha=0.5,color='g')
  #fig6.tight_layout()

  #fig1.savefig(fig_dir+'/Case{}_P.png'.format(Ncase))
  #fig2.savefig(fig_dir+'/Case{}_N.png'.format(Ncase))
  #fig3.savefig(fig_dir+'/Case{}_r.png'.format(Ncase))
  #fig4.savefig(fig_dir+'/Case{}_r.png'.format(Ncase))
  #fig5.savefig(fig_dir+'/Case{}_P_lin.png'.format(Ncase))
  #fig6.savefig(fig_dir+'/Case{}_N_lin.png'.format(Ncase))

  #plt.show()
  
  #np_X=np.array(df['X'][cut])
  #plt.plot(df['X'][cut],marker='^')
  #plt.plot(df['X'][cut_uniq],marker='o')
  #plt.plot(np_X,marker='o')
  #plt.show()

  #print(df[cutX0])
  #for uniX in uniXs:
  #  fig,ax=plt.subplots(figsize=(5,5))
  #  ax.set(aspect=1)
  #  cutX=(df['X']==uniX) & (df['PRE']>0)
  #  ax.scatter(df['Y'][cutX],df['Z'][cutX])
  #  #ax.set_xlim(-0.06,0.06)
  #  #ax.set_ylim(-0.06,0.06)
  #  ax.set_xlabel('Y [m(?)]')
  #  ax.set_ylabel('Z [m(?)]')
  #  ax.set_title('X={}, PRE>0'.format(uniX))
  #  fig.tight_layout()
  #  fig.savefig(fig_dir+'/YZpoint_X{:.4f}.png'.format(uniX))
  #  plt.close()

  #fig_dir='../fig/FJTtestY'
  #if not os.path.isdir(fig_dir):
  #  os.makedirs(fig_dir)
  #for uniY in uniYs:
  #  fig,ax=plt.subplots(figsize=(5,5))
  #  ax.set(aspect=1)
  #  cutY=(df['Y']==uniY) & (df['PRE']>0)
  #  ax.scatter(df['X'][cutY],df['Z'][cutY])
  #  #ax.set_xlim(-0.06,0.06)
  #  #ax.set_ylim(-0.06,0.06)
  #  ax.set_xlabel('X [m(?)]')
  #  ax.set_ylabel('Z [m(?)]')
  #  ax.set_title('Y={}, PRE>0'.format(uniY))
  #  fig.tight_layout()
  #  fig.savefig(fig_dir+'/XZpoint_Y{:.4f}.png'.format(uniY))
  #  plt.close()

  #for uniZ in uniZs:
  #  fig,ax=plt.subplots(figsize=(5,5))
  #  ax.set(aspect=1)
  #  cutZ=(df['Z']==uniZ) & (df['PRE']>0)
  #  ax.scatter(df['X'][cutZ],df['Y'][cutZ])
  #  #ax.set_xlim(-0.06,0.06)
  #  #ax.set_ylim(-0.06,0.06)
  #  ax.set_xlabel('Y [m(?)]')
  #  ax.set_ylabel('Z [m(?)]')
  #  ax.set_title('Z={}, PRE>0'.format(uniZ))
  #  fig.tight_layout()
  #  fig.savefig(fig_dir+'/XYpoint_Z{:.4f}.png'.format(uniZ))
  #  plt.close()

def plot_summarycsv(filename,outpdf='summary.pdf'):
  fig_dir='../fig/FJTplots'
  if not os.path.isdir(fig_dir):
    os.makedirs(fig_dir)

  pp=PdfPages(fig_dir+'/'+outpdf)

  df=pd.read_csv(filename)
  vals=["P [Pa]","N(/cm^3)","Mach"]
  x_min=min(df['X'])
  x_max=max(df['X'])
  x_margin=0.025

  for val in vals:
    fig1,ax1=plt.subplots(figsize=(10,5))
    fig2,ax2=plt.subplots(figsize=(10,5))
    for ca in range(1,6):
      label='Case{}'.format(ca)
      cut=(df["case"]==ca)
      cut_lin=(cut)&(df["X"]>0.1)
      ax1.plot(df["X"][cut]    ,df[val][cut]    ,label='Case{}'.format(ca),alpha=0.5)
      ax2.plot(df["X"][cut_lin],df[val][cut_lin],label='Case{}'.format(ca),alpha=0.5)

    ax1.set_title(val)
    ax1.set_xlabel('X [m]')
    ax1.set_ylabel(val)
    ax1.set_yscale('log')
    ax1.set_xlim(x_min-x_margin,x_max+x_margin)
    ax1.grid(color='0.5', linestyle='--', linewidth=0.5)
    ax1.axvline(0,alpha=0.5,color='r')
    ax1.axvline(x_max,alpha=0.5,color='r')
    ax1.axvline(0.1265,alpha=0.5,color='g')
    ax1.legend()
    fig1.tight_layout()

    ax2.set_title(val)
    ax2.set_xlabel('X [m]')
    ax2.set_ylabel(val)
    ax2.set_xlim(x_min-x_margin,x_max+x_margin)
    ax2.grid(color='0.5', linestyle='--', linewidth=0.5)
    ax2.axvline(0,alpha=0.5,color='r')
    ax2.axvline(x_max,alpha=0.5,color='r')
    ax2.axvline(0.1265,alpha=0.5,color='g')
    ax2.legend()
    fig2.tight_layout()
    pp.savefig(fig1)
    pp.savefig(fig2)
    plt.close()

  pp.close()

if __name__=="__main__":
  #Ncase=1
  #for Ncase in range(1,6):
  #  print('Case{}'.format(Ncase))
  #  filename="../data/delivery20240529/case{0}/Case{0}_currentFlow.tec".format(Ncase)
  #  names=["X","Y","Z","U","V","W","RHO","PRE","TEM","EE","N(/cm^3)","Mach"]
  #  outcsvname='../data/delivery20240529/summary_along_Xaxis.csv'
  #  plot_XYZ(filename,names,Ncase=Ncase,outcsvname=outcsvname)
  #  plt.close('all')

  #filename='../data/delivery20240529/summary_along_Xaxis.csv'
  #outpdf='summary_along_Xaxis.pdf'
  #plot_summarycsv(filename,outpdf=outpdf)

