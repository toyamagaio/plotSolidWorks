import sys
import os
import numpy as np
import pandas as pd

datadir='C:/Users/yt14p/Dropbox/work/ddmu_paper/'

def plot_XYplane(filename):
  df=pd.read_csv(filename)
  cut=(df['']==0)

  fig, ax=plt.subplots()
  CS = ax.contourf(X, Y, Z)
  fig.colorbar(CS)#colorbar
  plt.show()

def print_author(filename, sheet_name,output,aff_dict):
  df=pd.read_excel(datadir+'/'+filename,sheet_name)
  df = df.fillna(' ')

  FirstAuthor='Toyama'
  df['sort_key'] = df['Family name'].apply(lambda x: 0 if x == FirstAuthor else 1)
  df = df.sort_values(by=['sort_key', 'Family name'],ignore_index=True).drop('sort_key', axis=1)

  print(df)
  file_text=open(datadir+output,'w')
  affil_n=1
  affil_list=list()
  for i in range(len(df.index)):
    #print(r'\author[{0}]{{\fnm{{{1}}} \sur{{{2}}}}}'.format(i+1,df['Depertment'][i],df['Organization'][i]),file=file_text)
    affil_num=''
    IDs=str(df['AffiliationID'][i])
    for ID in IDs.split(','):
      intID=int(ID)
      affil=aff_dict[intID]
      if intID in affil_list:
        index=affil_list.index(intID)
        if affil_num =='':
          affil_num=str(index+1)
        else:
          affil_num=affil_num+','+str(index+1)
      else:
        affil_list.append(intID)
        if affil_num =='':
          affil_num=str(affil_n)
        else:
          affil_num=affil_num+','+str(affil_n)
        affil_n+=1
    print(r'\author[{0}]{{{1}}}'.format(affil_num,df['Name'][i]),file=file_text)

  for i,n in enumerate(affil_list):
    print(r'\affil[{0}]'.format(i+1)+aff_dict[n],file=file_text)


  file_text.close()

def print_affiliation(filename, sheet_name,output):
  df=pd.read_excel(datadir+'/'+filename,sheet_name)
  df = df.fillna(' ')
  print(df)

  aff_dict={}

  file_text=open(datadir+output,'w')
  for i in range(len(df.index)):
    #print(i)
    #print('affil[{0}]\{orgdiv{1}\}'.format(i,df['Depertment'][i]))
    print(r'\affil[{0}]{{\orgdiv{{{1}}}, \orgname{{{2}}}, \orgaddress{{\city{{{3}}}, \postcode{{{4}}}, \state{{{5}}}, \country{{{6}}}}}}}'.format(i+1,df['Depertment'][i],df['Organization'][i],df['City'][i],df['PostCode'][i],df['State'][i],df['Country'][i]),file=file_text)

    ID=df['ID'][i]
    affi=r'{{\orgdiv{{{1}}}, \orgname{{{2}}}, \orgaddress{{\city{{{3}}}, \postcode{{{4}}}, \state{{{5}}}, \country{{{6}}}}}}}'.format(i+1,df['Depertment'][i],df['Organization'][i],df['City'][i],df['PostCode'][i],df['State'][i],df['Country'][i])

    aff_dict[ID]=affi
  file_text.close()

  print(aff_dict)
  return aff_dict

if __name__=="__main__":
  filename='collaboration_list.xlsx'
  sheet_name='affiliation'
  output='aff.txt'
  aff_dict=print_affiliation(filename,sheet_name,output)

  sheet_name='20230310 (For mudd, ICPEAC2023)'
  output='auth.txt'
  print_author(filename,sheet_name,output,aff_dict)
