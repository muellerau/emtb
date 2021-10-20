#!/usr/bin/python3

# empip_class2img.py
# create overview image of 3D volumes

iversion = 'v0.1'

#import os
import subprocess
import argparse
import math


# parsing CLI options
parser = argparse.ArgumentParser(description=iversion+' - Generate image of 3D volumes arranged on a grid.')
parser.add_argument('vg_volumes', metavar='V', nargs='+',
                    help='path(s) to 3D volume(s)')
parser.add_argument('-c, --columns', metavar='C', nargs=1, dest='vg_col', default=0,
                    help='Number of columns in which to arrange volumes (default: single row)')
parser.add_argument('-s, --spacing', metavar='S', nargs=1, type=int, dest='vg_spacing', default=200,
                    help='Spacing between grid points, integer number (default: 200)')
parser.add_argument('-o', metavar='OUTDIR', nargs=1, dest='vg_outdir', default='.',
                    help='Output directory (default: current)')

args = parser.parse_args()

# main

def ck_env(prgs):
    fp=[] # found program
    np=[] # unavailable program
    if not isinstance(prgs, list): raise()
    for p in prgs:
        pout = subprocess.run(['which',p])
        if pout.returncode != 0:
            np+=[p]
        else:
            fp+=[p]
    return fp,np

# check prerequisites
reqprgs = ck_env(['chimerax'])
if len(reqprgs[1]) > 0:
    print('The following programs were not found:')
    for i in reqprgs[1]:
        print(i+'\n')
    print('Please check your working environment and/or install the required programs to continue.')

### chimerax command-line constructor

chx_inicmd = 'chimerax --nogui'

# collect volumes
volall='open '

for v in args.vg_volumes:
    volall+=str(v)+' '

# arrange volumes
spacer=''
vol_num=len(args.vg_volumes)
if args.vg_col == 0:
    img_rows=1
else:
    img_rows=math.ceil(vol_num/img_rows)

vol_counter=1
for r in range(0, img_rows):
    for c in range(0, args.vg_col):
        if vol_counter > vol_num: continue
        spacer+='move 1,0,0 '+str(vg_spacing*c)+' models #1.'+str(vol_counter)+' ' # move column
        spacer+='move 0,1,0 -'+str(vg_spacing*r)+' models #1.'+str(vol_counter)+' ' # move row
        vol_counter+=1

# stylize models
style=''
try:
    args.vg_color
except:
    pass
else:
    style+='color '+str(args.vg_color)

# save image
img='save '+str(args.vg_outdir)+'/arranged_volumes.png'
    
# build final cmd
chx_cmd = chx_inicmd+' -c "set bgColor white '+volall+spacer+style+' view '+img+'"'
print(chx_cmd)

# execute
subprocess.run(chx_cmd.split())

exit()