#!/usr/bin/env python3

#######################################################
# Data collector for relion Class3D jobs
# (c) 2022 - Andreas U Mueller - use at your own risk
#
# Usage: script.py path/to/Class3D/jobXXX/
#
#######################################################


import starfile
import sys
import glob
import pandas as pd

try:
    idir = str(sys.argv[1]).rstrip('/')
except Exception as e:
    sys.exit('Error: please provide correct input.\nUsage: rln_class3d_timeline.py path/to/Class3D/jobXXX/')

ifiles = glob.glob(idir + '/run*it???_model.star')

if not ifiles:
    sys.exit('Error: file list empty.\nUsage: rln_class3d_timeline.py path/to/Class3D/jobXXX/')

allmodclass = [starfile.read(f, read_n_blocks = 3)['model_classes'] for f in ifiles]

starcol = list(allmodclass[0].keys())
starcol.remove('rlnReferenceImage')

for each in allmodclass:
    each['iteration'] = each.rlnReferenceImage.str.extract('it(\d{3})')[0].str.lstrip('0').replace('', 0).astype('int')
    each['rlnClass'] = each.rlnReferenceImage.str.extract('class(\d{3})')[0].str.lstrip('0').astype('int')

nr_classes = allmodclass[0]['rlnClass']

allit = pd.concat(allmodclass)
allit.sort_values(['iteration','rlnClass'], ignore_index = True, inplace = True)

for h in starcol:
    output = pd.concat([allit.loc[allit['rlnClass'] == c, [str(h), 'iteration']].reset_index(drop=True).rename(columns={str(h):'class_'+str(c)}) for c in nr_classes], axis = 1)
    output = output.loc[:, ~output.columns.duplicated()].sort_index(axis = 1 ,ascending = False).copy().drop_duplicates(subset='iteration')
    outfile = idir+'/'+str(h)+'.txt'
    output.to_csv(outfile, sep = '\t', index = False)
    print('Written ' + outfile)

sys.exit(0)