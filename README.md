# emtb
### (cryo)EM toolbox

A variety of helper scripts and useful programs to accelerate cryoEM data processing.

Note: Files/scripts not listed below may be incomplete or placeholders and not ready for production.
As usual, use at your own risk.


## validate_cif_seq.py
Check sequences in the cif _entity_poly section against a FASTA reference.
Useful for PDB depositions/author approval step.

requirements: Biopython

## dump_gridfs.py
Extract files from cryoSPARC <=v4 gridFS data.

requirements: none

## check-pdb-seq.py
Validate model sequence in pdb file against reference sequences

Extracts sequence information for each chain from pdb file and compares against FASTA file containing the reference sequences; only reports mismatches, not gaps; only compares sequences/chains that exist in both model and reference sequence file (fasta headers must be named >refchain_A, >refchain_B, etc for correct assignment).

Reference sequences in FASTA format must be labeled as
refchain_A, refchain_B, refchain_C, and so on
in the header. Example:
```
>refchain_A
MLSHNDNENRHSNHDSWIASDIDPLQ
```

requirements: Biopython

## micronail
Generate micrograph thumbnails

Helpful wrapper for relion_image_handler to generate several thumbnails of randomly selected micrographs.

requirements: relion

## lrcc
Local Resolution Control Center (LRCC)

Batch processor for blocres and blocfilt on cryoSPARC job output.

Batch process cryoSPARC job output with local resolution and local
filtering using blocres/blocfilt.

## shoeshine
Prepare a cryoSPARC job for Bayesian polishing in Relion.

Requirements: pyem >= 20220427

## rln_class3d_timeline.py

Collect relion statistics from all iterations in text files for downstream actions (e.g. plotting).

```
Usage: rln_class3d_timeline.py path/to/Class3D/jobXXX/
```

## rln_splitclass.py

Split particle stacks from relion data.star files by class.
Also, produces output with particles reverted to original (if particle subtraction was done).

```
Usage: rln_splitclass.py path/to/Class3D/jobXXX/
Alternate: rln_splitclass.py path/to/Class3D/jobXXX/run_XXX_data.star
```

## 3dfsc_cs.bash

Small wrapper to run 3DFSC on cryoSPARC jobs (takes the last iteration).
Uses refinement mask and computes on GPU.

```
Usage: 3dfsc_cs.bash path/to/csproject/JXXX/ pixel_size
```

## 3dfsc_histplot.py

Customized graph plotting from output of the 3DFSC program (https://github.com/nysbc/Anisotropy)

Tan, Y., Baldwin, P., Davis, J. et al. Addressing preferred specimen orientation in single-particle cryo-EM through tilting. Nat Methods 14, 793–796 (2017). https://doi.org/10.1038/nmeth.4347

Dependencies: numpy, matplotlib

## pdb_analyze-bfactors.py

Get an overview of your the bfactor values in your pdb file.
With outlier report and histogram plot functionality.

```
Usage: pdb_analyze-bfactors.py mymodel.pdb --hist
```
