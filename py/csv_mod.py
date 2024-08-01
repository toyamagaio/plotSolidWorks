import os
import sys
import pandas as pd
import re
def remove_non_numeric(s):
    #return re.sub(r'\D', '', s)
    return re.sub(r'[^0-9.keE-]', '', s)

def remove_after_k(s):
    # Regular expression pattern to match 'k' and everything after it
    pattern = r'k.*'
    # Search for the pattern in the string
    match = re.search(pattern, s)
    if match:
        # If a match is found, return the part of the string up to and including 'k'
        return s[:match.start()]
    else:
        # If 'k' is not found, return the original string
        return s

#filepath='../../mach_jet/test0718/output.csv'
#filepath='../../mach_jet/test0731/out.csv'
def main():
  if len(sys.argv) < 2:
    print('input file is not specified.')
    print('usage: cov_mod.py {inputcsvfile}')
    sys.exit(1)
  else:
    filepath=sys.argv[1]
  
  if not os.path.isfile(filepath):
    print(f'{filepath} does not exit')
    sys.exit(1)
  df=pd.read_csv(filepath)
  print(df.keys())
  #print(df['P1'])
  print(df)
  
  #df['P1']=re.sub(r'[^a-zA-Z]','',df['P1'])
  df=df.applymap(remove_non_numeric)
  #print(df['P1'])
  print(df)
  df=df.applymap(remove_after_k)
  print(df)
  df.to_csv(filepath.replace('.csv','_mod.csv'),index=False)

if __name__=="__main__":
  main()
