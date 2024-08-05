import sys
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

# file path
header_csv_path = '../data/Header.csv'
#csv_path = '../data/log/MLF2024Feb2024_01_09_18;34.csv'
csv_path = '../data/RIBF308test2024_07_29_14;48.csv'
args=sys.argv
if len(args)>1:
  csv_path=args[1]

y_value='50 mK FAA Temperature'

# reset plot
fig, ax = plt.subplots(3,1)
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
plt.xlabel('Time')
plt.ylabel(y_value)
plt.title('Real-time Temperature Plot')

# reset data frame
df = pd.read_csv(header_csv_path,header=0,skiprows=[1],skipinitialspace=True)

# previous num of rows
last_row = 3 #header part

def offline_plot():
  global df, last_row
  print('update_plot... last_row {}'.format(last_row))

  # read newest data from csv file
  new_data = pd.read_csv(csv_path, names=df.keys(), header=None, skiprows=last_row)
  df = pd.concat([df,new_data], ignore_index=True)
  
  # update graph
  ax[0].plot(df['Hours after Start'], df[y_value], marker='o',linestyle='')
  ax[0].set_xlabel('Hours')
  ax[0].set_ylabel(y_value)
  #ax[0].set_title('Real-time Temperature Plot')

  ax[1].plot(df['Hours after Start'], df['PID Setpoint'], marker='o',linestyle='')
  ax[1].set_xlabel('Hours')
  ax[1].set_ylabel('PID Setpoint')

  ax[2].plot(df['Hours after Start'], df['PID Output'], marker='o',linestyle='')
  ax[2].set_xlabel('Hours')
  ax[2].set_ylabel('PID Output')

  latest_time=np.float(df['Hours after Start'][-1:])
  print('latest_time',latest_time)
  last_1min_cut= (df['Hours after Start'] > latest_time-1./60.)
  last_2min_cut= (df['Hours after Start'] > latest_time-2./60.)
  last_5min_cut= (df['Hours after Start'] > latest_time-5./60.)
  start_hour=1700./60.
  end_hour  =1774./60.
  #test_cut=(df['Hours after Start']>start_hour) &(df['Hours after Start']<end_hour)
  test_cut=(df['PID Setpoint']>0.05) & (df['Hours after Start']>1700./60.)
  current_hour=start_hour
  list_std_2min=list()
  list_hour=list()
  while(current_hour<end_hour):
    cut=(df['PID Setpoint']>0.05) & (df['Hours after Start']>current_hour) &(df['Hours after Start']<current_hour+2./60.)
    std_2min=np.std(df[y_value][cut])
    list_std_2min.append(std_2min)
    list_hour.append(current_hour)
    current_hour+=1./60.
    #print(len(list_std_2min),len(list_hour))

  ax1.clear()
  ax1.plot(60*(df['Hours after Start'][test_cut]), df[y_value][test_cut], marker='o')
  ax1.set_xlabel('Min')
  ax1.set_ylabel(y_value)
  ax1.set_title(f'Temperature Plot ({start_hour}h--{end_hour}h)')
  # get data range
  x_lim = ax1.get_xlim()
  y_lim = ax1.get_ylim()
  # text position
  x_pos = x_lim[0] + 0.02 * (x_lim[1] - x_lim[0])
  y_pos = y_lim[0] + 0.98 * (y_lim[1] - y_lim[0])

  ax1.plot(60*(df['Hours after Start'][test_cut]), df[y_value][test_cut], marker='o')
  ax1.set_xlabel('Min')
  ax1.set_ylabel(y_value)
  ax1.set_title(f'Temperature Plot ({start_hour:.2f}h--{end_hour:.2f}h)')
  
  ##std of last 1min, 2min, last 5min
  std_test     =np.std(df[y_value][test_cut])
  print('std: {:.3e} K'.format(std_test))
  ax1.text(x_pos,y_pos,'std in this plot: {:.2e} K'.format(std_test),ha='left',va='top')

  ax2.plot(60.*np.asarray(list_hour), list_std_2min, marker='o')
  ax2.set_xlabel('Min')
  ax2.set_ylabel('Std of '+y_value)
  ax2.set_title(f'Temperature std in 2min ({start_hour:.2f}h--{end_hour:.2f}h)')

  # save current num of rows
  last_row += len(new_data)

offline_plot()
plt.show()
