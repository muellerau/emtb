#!/usr/bin/env python3

"""
Compare reference FASTA sequences against sequences in mmCIF _entity_poly.

Uses Biopython's built-in MMCIF2Dict parser.

Uses:
    _entity_poly.pdbx_seq_one_letter_code_can

Reports:
    _entity_poly.pdbx_strand_id

Skips comparisons where lengths differ by >10%.
Uses direct positional identity with length penalties.

Requirements:
    pip install biopython

Usage:
    python compare_sequences.py refs.fasta target.cif
"""

import sys
import re
from Bio import SeqIO
from Bio.PDB.MMCIF2Dict import MMCIF2Dict


# --------------------------------------------------
# Utilities
# --------------------------------------------------

def clean_seq(seq):
    seq = str(seq).replace("?", "")
    seq = re.sub(r"\s+", "", seq)
    return seq.strip().upper()


def as_list(x):
    if isinstance(x, list):
        return x
    return [x]


def length_ok(seq1, seq2, tolerance=0.10):
    if not seq1 or not seq2:
        return False
    return abs(len(seq1) - len(seq2)) / max(len(seq1), len(seq2)) <= tolerance


# --------------------------------------------------
# Identity
# --------------------------------------------------

def percent_identity(seq1, seq2):
    """
    Direct positional identity.

    IMPORTANT:
    Extra residues and substitutions reduce identity.

    Example:
        AAAA vs AAAAB = 80%
        AAAA vs AABA  = 75%
    """
    l1 = len(seq1)
    l2 = len(seq2)

    if l1 == 0 or l2 == 0:
        return 0.0

    n = min(l1, l2)

    matches = 0
    for a, b in zip(seq1[:n], seq2[:n]):
        if a == b:
            matches += 1

    # use longer length so insertions/deletions penalize score
    return 100.0 * matches / max(l1, l2)


# --------------------------------------------------
# FASTA
# --------------------------------------------------

def load_references(fasta_file):
    refs = []

    for rec in SeqIO.parse(fasta_file, "fasta"):
        seq = clean_seq(str(rec.seq))
        if seq:
            refs.append((rec.id, seq))

    return refs


# --------------------------------------------------
# mmCIF
# --------------------------------------------------

def load_queries_from_cif(cif_file):
    cif = MMCIF2Dict(cif_file)

    try:
        seqs = as_list(cif["_entity_poly.pdbx_seq_one_letter_code_can"])
        strands = as_list(cif["_entity_poly.pdbx_strand_id"])
    except KeyError:
        return []

    queries = []

    for strand, seq in zip(strands, seqs):
        seq = clean_seq(seq)
        if seq:
            queries.append((strand, seq))

    return queries


# --------------------------------------------------
# Compare
# --------------------------------------------------

def compare_sequences(refs, queries, threshold=70.0):
    matched = set()

    for ref_id, ref_seq in refs:
        best_query = None
        best_pid = -1.0

        for query_name, query_seq in queries:

            if not length_ok(ref_seq, query_seq, 0.10):
                continue

            pid = percent_identity(ref_seq, query_seq)

            if pid > best_pid:
                best_pid = pid
                best_query = query_name

        if best_query is not None and best_pid >= threshold:
            print(
                f"{ref_id} <-> {best_query}, "
                f"{best_pid:.2f}% "
                f"(len {len(ref_seq)} vs {len(dict(queries)[best_query])})"
            )
            matched.add(best_query)
        else:
            print(f"{ref_id} <-> NO MATCH")

    for query_name, _ in queries:
        if query_name not in matched:
            print(f"UNMATCHED QUERY: {query_name}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_sequences.py refs.fasta target.cif")
        sys.exit(1)

    refs = load_references(sys.argv[1])
    queries = load_queries_from_cif(sys.argv[2])

    if not refs:
        print("No reference sequences found.")
        sys.exit(1)

    if not queries:
        print("No _entity_poly sequences found.")
        sys.exit(1)

    compare_sequences(refs, queries)


if __name__ == "__main__":
    main()


