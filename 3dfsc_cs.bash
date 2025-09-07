#!/bin/bash

export LC_ALL=C
SECONDS=0

currdir=$(pwd)
workdir="$1"
pxsize="$2"

cd "$workdir"
echo "wd:" $(pwd)

halfA=($(find . -name "*_map_half_A.mrc" | sort -r))
halfB=($(find . -name "*_map_half_B.mrc" | sort -r))
full=($(find . -name "*_map.mrc" | sort -r))
csmask=($(find . -name "*_mask_refine.mrc" | sort -r))

ThreeDFSC_Start.py --halfmap1="${halfA[0]}" --halfmap2="${halfB[0]}" --fullmap="${full[0]}" --mask="${csmask[0]}" --apix="$pxsize" --gpu

cd "$currdir"

echo "Completed 3DFSC job in $SECONDS seconds."

echo "wd:" $(pwd)

exit
