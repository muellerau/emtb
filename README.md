# emtb
## (cryo)EM toolbox
Level 5 - scripts, programs, superweapons

## Local Resolution Control Center (LRCC)
Batch processor for blocres and blocfilt on cryoSPARC job output.

Batch process cryoSPARC job output with local resolution and local
filtering using blocres/blocfilt.

Usage: lrcc [options] input_folder [output_folder]

Point to one or more directories that each contain the half maps and a
sharpened map.

Map files are recognized by pattern matching
half map A        *map_half_A.mrc
half map B        *map_half_B.mrc
sharpened map     *map_sharp.mrc
mask              *mask_refine.mrc

This is the pattern employed by cryoSPARC, so LRCC can process
map files directly from cryoSPARC job directories.

Positional arguments:
    input_folder
    output_folder
Optional arguments:
    -h                      Print this message.

    -b box_size             Choose kernel size for blocres/blocfilt
                             default: 20
    
    -f                      Flip output maps (uses chimerax).

    -j \"job1 job2 ...\"    Specify cryoSPARC jobs to process. If -j is
                             not used, LRCC will search the input
                             directory for maps and no batch processing
                             will be performed.

    -m mask.mrc             Provide a custom mask for blocres/blocfilt.
                             default: *mask_refine.mrc

    -M                      Turn off masking and compute full box.

    -n processes            Number of processes to parallelize.
                             default: 1

    -o x,y,z                Set origin coordinates.
                             default: 0,0,0 ()

    -s sampling             Set bloc sampling. Generally, use the map
                             pixel size (A/px).

    -r resolution           Set maximum resolution in data (in Angstrom).
                             Generally, twice the pixel size.

    -x \"-arg1 -arg2 ...\"  Pass additional arguments to blocres.

    -y \"-arg1 -arg2 ...\"  Pass additional arguments to blocfilt.
 
