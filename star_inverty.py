#!/bin/env python3

###
# written by Andreas Mueller
# 2024-11-14
# use at your own risk
###

import starfile
import sys
import os

shiny_path = sys.argv[1]
ysize = int(sys.argv[2])
if not os.path.exists(shiny_path):
    print("ERROR: file does not exist.")
    exit()

if not isinstance(ysize, (int, float, complex)):
    print("ERROR: micrograph y dimension not recognized.")
    exit()

shiny_data = starfile.read(shiny_path)
inverted = shiny_data['particles']['rlnCoordinateY'].apply(lambda x: ysize - x)

shiny_data['particles'].loc[:, 'rlnCoordinateY'] = inverted

outpath = '.'.join(shiny_path.split('.')[:-1]) + '_inverty.star'

starfile.write(shiny_data, outpath)

exit()