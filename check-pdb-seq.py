#!/usr/bin/env python3

import argparse
import os
import tempfile
import subprocess
from Bio import SeqIO, PDB
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.PDB.Polypeptide import PPBuilder
from Bio import Align

#def extract_pdb_sequences(pdb_file, output_fasta=None):
#    parser = PDB.PDBParser(QUIET=True)
#    structure = parser.get_structure("PDB_structure", pdb_file)
#    ppb = PPBuilder()
#    records = []
#
#    for model in structure:
#        for chain in model:
#            chain_id = chain.id
#            peptides = ppb.build_peptides(chain)
#            if peptides:
#                seq = ''.join(str(pp.get_sequence()) for pp in peptides)
#                record = SeqRecord(Seq(seq), id=f"pdbchain_{chain_id}", description="")
#                records.append(record)
#
#    if output_fasta:
#        SeqIO.write(records, output_fasta, "fasta")
#
#    return {r.id.replace("pdbchain_", ""): r for r in records}


def extract_pdb_sequences(pdb_file, output_fasta=None):
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("PDB_structure", pdb_file)
    ppb = PPBuilder()
    records = []

    # Maps for DNA/RNA
    nucleotide_codes = {
        'A': 'A', 'C': 'C', 'G': 'G', 'T': 'T', 'U': 'U',
        'DA': 'A', 'DC': 'C', 'DG': 'G', 'DT': 'T', 'DU': 'U',
        'ADE': 'A', 'CYT': 'C', 'GUA': 'G', 'THY': 'T', 'URA': 'U'
    }

    for model in structure:
        for chain in model:
            chain_id = chain.id

            # Try protein sequence via polypeptide builder
            peptides = ppb.build_peptides(chain)
            if peptides:
                seq = ''.join(str(pp.get_sequence()) for pp in peptides)
                if seq:
                    record = SeqRecord(Seq(seq), id=f"pdbchain_{chain_id}", description="")
                    records.append(record)
                    continue  # Skip to next chain

            # If not protein, try nucleotide sequence
            nt_seq = []
            for residue in chain:
                resname = residue.get_resname().strip()
                if resname in nucleotide_codes:
                    nt_seq.append(nucleotide_codes[resname])
            if nt_seq:
                record = SeqRecord(Seq(''.join(nt_seq)), id=f"pdbchain_{chain_id}", description="")
                records.append(record)

    if output_fasta:
        SeqIO.write(records, output_fasta, "fasta")

    return {r.id.replace("pdbchain_", ""): r for r in records}


def load_reference_sequences(ref_fasta):
    ref_records = SeqIO.to_dict(SeqIO.parse(ref_fasta, "fasta"))
    # Remove "refchain_" prefix
    return {k.replace("refchain_", ""): v for k, v in ref_records.items()}

def align_sequences_biopython(seq1, seq2):
    aligner = Align.PairwiseAligner()
    aligner.mode = 'global'
    aligner.open_gap_score = -10
    aligner.extend_gap_score = -0.5

    alignments = aligner.align(seq1, seq2)
    return alignments[0]  # Return the best alignment

def count_mismatches_from_alignment(alignment):
    aligned_seq1 = alignment[0]
    aligned_seq2 = alignment[1]

    mismatches = compare_sequences(aligned_seq1, aligned_seq2)

    return mismatches, alignment.format()

def compare_sequences(aligned_seq1, aligned_seq2):
    mismatches = 0
    for a, b in zip(aligned_seq1, aligned_seq2):
        if a != '-' and b != '-' and a != b:
            mismatches += 1
    return mismatches

def main():
    parser = argparse.ArgumentParser(description="Compare PDB chain sequences to reference FASTA sequences")
    parser.add_argument("pdb_file", help="Input PDB file")
    parser.add_argument("ref_fasta", help="Reference FASTA file")
    parser.add_argument("-o", "--output", help="Output alignment file", default="alignments.txt")
    parser.add_argument("--save-pdb-fasta", help="Optionally save extracted PDB sequences as FASTA")

    args = parser.parse_args()

    print("Parsing PDB and extracting sequences...")
    pdb_seqs = extract_pdb_sequences(args.pdb_file, args.save_pdb_fasta)

    print("Reading reference sequences...")
    ref_seqs = load_reference_sequences(args.ref_fasta)

    print("Running alignments and comparing sequences...")
    with open(args.output, "w") as out_f:
        for chain_id, pdb_record in pdb_seqs.items():
            if chain_id not in ref_seqs:
                print(f"WARNING: No reference sequence for chain {chain_id}")
                continue

            ref_record = ref_seqs[chain_id]
            try:
                alignment = align_sequences_biopython(str(pdb_record.seq), str(ref_record.seq))
                mismatches, formatted_alignment = count_mismatches_from_alignment(alignment)
                
                out_f.write(f"# Alignment for chain {chain_id}\n")
                out_f.write(formatted_alignment)
                out_f.write(f"# Mismatches (excluding gaps): {mismatches}\n\n")
                print(f"Chain {chain_id}: {mismatches} mismatches")

            except subprocess.CalledProcessError as e:
                print(f"ERROR: Needle alignment failed for chain {chain_id}")
                continue

    print(f"\nDone. Alignments written to: {args.output}")
    if args.save_pdb_fasta:
        print(f"PDB sequences saved to: {args.save_pdb_fasta}")

if __name__ == "__main__":
    main()
