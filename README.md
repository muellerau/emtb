# emtb
### (cryo)EM toolbox

A variety of helper scripts and useful programs to accelerate cryoEM data processing.

Note: Files/scripts not listed below may be incomplete or placeholders and not ready for production.
As usual, use at your own risk.


## micronail
Generate micrograph thumbnails

Helpful wrapper for relion_image_handler to generate several thumbnails of randomly selected micrographs.

written by Andreas U Mueller - 2025

requirements: relion

## lrcc
Local Resolution Control Center (LRCC)

Batch processor for blocres and blocfilt on cryoSPARC job output.

written by Andreas U Mueller - 2021

Batch process cryoSPARC job output with local resolution and local
filtering using blocres/blocfilt.

## shoeshine
Prepare a cryoSPARC job for Bayesian polishing in Relion.

written by Andreas U Mueller - 2022

Requirements: pyem >= 20220427

## rln_class3d_timeline.py

Collect relion statistics from all iterations in text files for downstream actions (e.g. plotting).

written by Andreas U Mueller - 2022
```
Usage: rln_class3d_timeline.py path/to/Class3D/jobXXX/
```

## rln_splitclass.py

Split particle stacks from relion data.star files by class.
Also, produces output with particles reverted to original (if particle subtraction was done).

written by Andreas U Mueller - 2022

```
Usage: rln_splitclass.py path/to/Class3D/jobXXX/
Alternate: rln_splitclass.py path/to/Class3D/jobXXX/run_XXX_data.star
```

## 3dfsc_cs.bash

Small wrapper to run 3DFSC on cryoSPARC jobs (takes the last iteration).
Uses refinement mask and computes on GPU.

written by Andreas U Mueller - 2022

```
Usage: 3dfsc_cs.bash path/to/csproject/JXXX/ pixel_size
```

## 3dfsc_histplot.py

Customized graph plotting from output of the 3DFSC program (https://github.com/nysbc/Anisotropy)

Tan, Y., Baldwin, P., Davis, J. et al. Addressing preferred specimen orientation in single-particle cryo-EM through tilting. Nat Methods 14, 793–796 (2017). https://doi.org/10.1038/nmeth.4347

written by Andreas U Mueller - 2025

Dependencies: numpy, matplotlib

## pdb_analyze-bfactors.py

Get an overview of your the bfactor values in your pdb file.
With outlier report and histogram plot functionality.

written by Andreas U Mueller - 2025

```
Usage: pdb_analyze-bfactors.py mymodel.pdb --hist
```
