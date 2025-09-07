#!/usr/bin/env python3

#######################################################
# Split classes from relion Class3D jobs
# (c) 2022 - Andreas U Mueller - use at your own risk
#
# Usage: script.py path/to/Class3D/jobXXX/[run_XXX_data.star]
#
#######################################################

import starfile
import os
import sys
import glob
import pandas as pd

scrusage = 'Usage: rln_splitclass.py path/to/Class3D/jobXXX/[run_XXX_data.star]'


try:
    idir = str(sys.argv[1]).rstrip('/')
except Exception as e:
    sys.exit('Error: please provide correct input.\n'+scrusage)

if idir[-5:] != '.star':
    ifiles = glob.glob(idir + '/run*it???_data.star')

    if not ifiles:
        sys.exit('Error: file list empty.\n'+scrusage)

    ifiles.sort(key=lambda x: x[-15:])
    exfile = ifiles[-1]
else:
    exfile = idir

if (exfile[-9:] != 'data.star'):
    sys.exit('Error: must provide *data.star file or Class3D job folder.\n'+scrusage)

print('Reading file '+str(exfile))

exstar = starfile.read(exfile)

nclass = list(exstar['particles']['rlnClassNumber'].drop_duplicates())

if ('rlnImageOriginalName' not in exstar['particles'].keys()):
    norevert = True
else:
    norevert = False

opath = os.path.dirname(exfile)
if norevert:
    odir = [opath+'/select']
else:
    odir = [opath+'/select', opath+'/select_reverted']

for x in odir:
    try:
        os.mkdir(x)
    except FileExistsError:
        pass

# generate per class star files
print('Splitting classes...')
for i in nclass:
    outstar = exstar.copy()
    outstar['particles'] = exstar['particles'].loc[exstar['particles'].rlnClassNumber == i]
    
    olen = int(len(outstar['particles'])/1000)
    oname = odir[0] + '/' + os.path.basename(exfile).split('.')[0] + '_class-' + str(i) + '_' + str(olen) + 'k.star'
    starfile.write(outstar, oname)
    print('Written class '+str(i)+' with '+str(olen)+'k particles to')
    print('   '+oname)

if norevert: sys.exit(0)

# generated reverted star files
print('Reverting to original particle images...')
for i in nclass:
    outstar = exstar.copy()
    outstar['particles'] = exstar['particles'].loc[exstar['particles'].rlnClassNumber == i].rename(columns={'rlnImageName':'rlnImageName_old','rlnImageOriginalName':'rlnImageOriginalName_old'}).rename(columns={'rlnImageName_old':'rlnImageOriginalName','rlnImageOriginalName_old':'rlnImageName'})
    
    olen = int(len(outstar['particles'])/1000)
    oname = odir[1] + '/' + os.path.basename(exfile).split('.')[0] + '_class-' + str(i) + '_' + str(olen) + 'k_reverted.star'
    starfile.write(outstar, oname)
    print('Written class '+str(i)+' with '+str(olen)+'k particles to')
    print('   '+oname)

sys.exit(0)