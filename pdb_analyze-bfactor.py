#!/usr/bin/env python3

#################################
#
# pdb_analyze-bfactor.py
# analyze bfactor statistics of a pdb file
#
# (c) 2025 - Andreas U. Mueller
#
#     USE AT YOUR OWN RISK
#
#################################

import argparse
import matplotlib.pyplot as plt
from Bio import PDB
import os

# Set up argument parsing
parser = argparse.ArgumentParser(description="Analyze PDB B-factor statistics.")
parser.add_argument("pdb_file", help="Path to the PDB file")
parser.add_argument("--lower", type=float, default=None, help="Lower B-factor limit")
parser.add_argument("--upper", type=float, default=None, help="Upper B-factor limit")
parser.add_argument("--hist", action='store_true', help="Plot histogram")
parser.add_argument("--savetxt", action='store_true', help="Plot histogram")
args = parser.parse_args()

# Load and parse the PDB file
pdb_file = args.pdb_file
parser = PDB.PDBParser(QUIET=True)
structure = parser.get_structure("Protein", pdb_file)

# List to store B-factors
b_factors = []

# Extract B-factors from the PDB structure
for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                b_factor_i = atom.get_bfactor()
                b_factors.append(b_factor_i)
                
                # Report outliers based on the lower and upper limits
                if args.lower is not None and b_factor_i < args.lower:
                    print(f"Lower limit outlier: {model}, {chain}, {residue}, {atom}, B-factor = {b_factor_i}")
                if args.upper is not None and b_factor_i > args.upper:
                    print(f"Upper limit outlier: {model}, {chain}, {residue}, {atom}, B-factor = {b_factor_i}")


# Report overall average b-factor
print('Overall average b-factor = ', sum(b_factors) / len(b_factors))

if args.hist:
    # Plot histogram of B-factors
    plt.figure(figsize=(8, 6))
    counts, bin_edges, patches = plt.hist(b_factors, bins=50, edgecolor='black', color='skyblue')
    
    if args.savetxt:
        # Save to a text file
        with open(f'{os.path.splitext(os.path.basename(pdb_file))[0]}_bfactor_hist.txt', 'w') as f:
            f.write("Bin_lower_edge, Counts\n")
            for edge, count in zip(bin_edges[:-1], counts):  # We exclude the last bin edge because it's not used
                f.write(f"{edge},{count}\n")
    
    plt.title("Histogram of B-factors")
    plt.xlabel("B-factor")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()