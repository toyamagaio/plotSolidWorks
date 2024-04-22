import sys
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

# file path
header_csv_path = '../data/log/Header.csv'
#csv_path = '../data/log/MLF2024Feb2024_01_09_18;34.csv'
csv_path = '../data/log/MLF2024Feb2024_01_09_18;35.csv'
args=sys.argv
if len(args)>1:
  csv_path=args[1]

y_value='50 mK FAA Temperature'

# reset plot
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
plt.xlabel('Time')
plt.ylabel(y_value)
plt.title('Real-time Temperature Plot')

# reset data frame
df = pd.read_csv(header_csv_path,header=0,skiprows=[1],skipinitialspace=True)

# previous num of rows
last_row = 3 #header part

def update_plot(frame):
  global df, last_row
  print('update_plot... last_row {}'.format(last_row))

  # read newest data from csv file
  #new_data = pd.read_csv(csv_path, header=0, skiprows=last_row)
  new_data = pd.read_csv(csv_path, names=df.keys(), header=None, skiprows=last_row)
  #print(new_data)
  #print(new_data.keys())
  
  # nothing to do when data is empty
  if new_data.empty:
    print('empty data')
    return
  
  # add new data to DataFrame
  #df = df.append(new_data, ignore_index=True)
  df = pd.concat([df,new_data], ignore_index=True)
  
  # update graph
  ax.clear()
  ax.plot(df['Hours after Start'], df[y_value], marker='o')
  #print(df['Hours after Start'])
  #print(df[y_value])
  ax.set_xlabel('Hours')
  ax.set_ylabel(y_value)
  ax.set_title('Real-time Temperature Plot')

  latest_time=np.float(df['Hours after Start'][-1:])
  print('latest_time',latest_time)
  last_1min_cut= (df['Hours after Start'] > latest_time-1./60.)
  last_2min_cut= (df['Hours after Start'] > latest_time-2./60.)
  last_5min_cut= (df['Hours after Start'] > latest_time-5./60.)

  ax1.clear()
  ax1.plot(60*(df['Hours after Start'][last_2min_cut]-latest_time), df[y_value][last_2min_cut], marker='o')
  ax1.set_xlabel('Min')
  ax1.set_ylabel(y_value)
  ax1.set_title('Real-time Temperature Plot (last 2min)')
  # get data range
  x_lim = ax1.get_xlim()
  y_lim = ax1.get_ylim()
  # text position
  x_pos = x_lim[0] + 0.02 * (x_lim[1] - x_lim[0])
  y_pos = y_lim[0] + 0.98 * (y_lim[1] - y_lim[0])

  
  ##std of last 1min, 2min, last 5min
  std_last_1min=np.std(df[y_value][last_1min_cut])
  std_last_2min=np.std(df[y_value][last_2min_cut])
  std_last_5min=np.std(df[y_value][last_5min_cut])
  print('std_last_1min: {:.3e} K'.format(std_last_1min))
  print('std_last_2min: {:.3e} K'.format(std_last_2min))
  print('std_last_5min: {:.3e} K'.format(std_last_5min))
  #ax1.text(x_pos,y_pos,'std_last_2min: {:.3e} K'.format(std_last_2min))
  ax1.text(x_pos,y_pos,'std last 2min: {:.2e} K'.format(std_last_2min),ha='left',va='top')

  # save current num of rows
  last_row += len(new_data)

# start animation
#ani = FuncAnimation(fig, update_plot, interval=60000)  # update every 1min
ani = FuncAnimation(fig, update_plot, interval=10000)  # update every 10sec

#show graph
plt.show()
