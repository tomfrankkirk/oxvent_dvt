import numpy as np 
import glob 
import os.path as op 
import os 
import re 
from pdb import set_trace
import re 
import pandas as pd 

def load(from_dir, regexp, crop, colnames, **kwargs):
    if type(regexp) is str: 
        regexp = re.compile(regexp)
  
    data = {}
    for f in os.listdir(from_dir): 
        match = regexp.search(f)
        if match: 
            name = match.group()[:-crop] if crop else match.group()
            path = op.join(from_dir, f)
            d = np.genfromtxt(path, delimiter=',', **kwargs)
            d = pd.DataFrame(d, columns=colnames) 
            data[name] = d
            
    if not data: 
        print("Warning: didn't match any files")
    print(data.keys())
    return data 

def stack_uneven(arrays): 
    rows = max([ a.shape[0] for a in arrays ])
    others = arrays[0].shape[1:] 
    final = len(arrays) 
    out = np.empty((rows, *others, final)) 
    out[:] = np.nan 
    for aidx,arr in enumerate(arrays):
        out[:arr.shape[0],...,aidx] = arr 
    return out 