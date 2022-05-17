#!/usr/bin/python

#################################
#
# superSTAR.py
# manipulate particles like a star
#
# (c) 2021 - Andreas U. Mueller
#
#     USE AT YOUR OWN RISK
#
#################################

iversion = 'v0.1'

import sys
import starfile
import pandas

handletypes = ['particles', 'micrographs']

def sps_read(ifiles):
    # read input
    stars = []
    for f in ifiles:
        try:
            stars += [starfile.read(f, always_dict=True)]
        except FileNotFoundError:
            print("Skipping %s, file not found...", f)
    return stars

def sps_write(odf):
    # write output
    try:
        for each in odf:
            starfile.write(each, odir)
    except FileExistsError:
        # decide what to do
        pass
    else:
        pass
    return 0

def sps_deconvolve(stars, section):
    return [s[section] for s in stars]

def sps_join(stars, master, res_mm=False):
    joinedstar = OrderedDict()
    # need to do some sanity checks here ...
    joinedparticles = master['particles'].concat(sps_deconvolve(stars, 'particles'), ignore_index=True)
    joinedstar['optics'] = master['optics'] # rewrite to include any other blocks from the master
    joinedstar['particles'] = joinedparticles
    return joinedstar

def sps_splitunique(stars, col):
    fsplit = []
    for s in stars: # mutiple star file handling?
        spsplit = [s['particles'].loc(s['particles'].col==u) for u in set(s['particles'].col)]
        for x in spsplit:
            snew = OrderedDict()
            for k in s.keys():
                if k != 'particles':
                    snew[k] = s[k]
                else:
                    snew[k] = spsplit
            fsplit += [snew]
    return fsplit

def sps_main(args):
    
    if args.keep_optics_group is not None:
        pass
    
    if args.select_class is not None:
        # split into individual classes, then select desired one and save
        #sps_splitunique(stars, 'rlnClassNumber')
        pass
    
    return 0

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=iversion+' - Manipulate particles like a star.')
    parser.add_argument('istar', metavar='istar', nargs='+',
                        help='input star files')
    parser.add_argument('-c, --columns', metavar='C', nargs=1, dest='vg_col', default=0,
                        help='Merge input files on columns c1,c2,c3,...,cN')
    parser.add_argument('--info', metavar='C', nargs=1, dest='vg_col', default=0,
                        help='Print summary information about input files.')
    parser.add_argument('-b, --batch', metavar='S', nargs=1, type=int, dest='vg_spacing', default=200,
                        help='Process input files individually.')
    parser.add_argument('-j, --join', metavar='S', nargs=1, type=str,
                        help='Join all input files together on a master. Specify -d to remove duplicates.')
    parser.add_argument('-k, --keep-optics-groups', metavar='S', nargs=1, type=int, dest='vg_spacing', default=200,
                        help='default: True')
    parser.add_argument('-d', metavar='S', nargs=1, type=int, dest='vg_spacing', default=200,
                        help='Duplicate observer switch.')
    parser.add_argument('-r, --resolve-mismatch', metavar='S', nargs=1, type=int, dest='vg_spacing', default=200,
                        help='Method to resolve column mismatches. default: error')
    parser.add_argument('-s, --split-unique', metavar='S', nargs=1, type=str, default='rlnClassNumber'
                        help='[B] Split input files by unique values in specified column. default: rlnClassNumber')
    parser.add_argument('-o', metavar='OUTDIR', nargs=1, dest='ss_outdir', default='.',
                        help='Output directory (default: current)')

    sys.exit(sps_main(parser.parse_args()))
