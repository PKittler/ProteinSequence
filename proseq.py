#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
from collections import defaultdict

# amino acid codes: 3-letter-code to 1-letter-code
THREE_TO_ONE = {
    'ALA': 'A',
    'ARG': 'R',
    'ASN': 'N',
    'ASP': 'D',
    'CYS': 'C',
    'GLU': 'E',
    'GLN': 'Q',
    'GLY': 'G',
    'HIS': 'H',
    'ILE': 'I',
    'LEU': 'L',
    'LYS': 'K',
    'MET': 'M',
    'PHE': 'F',
    'PRO': 'P',
    'SER': 'S',
    'THR': 'T',
    'TRP': 'W',
    'TYR': 'Y',
    'VAL': 'V'
}

def parse_pdb_sequence(pdb_filepath):
    """
    Extract the amino acid sequence(s) from a PDB file.

    Args:
        pdb_filepath (str): Path to the PDB file.

    Returns:
        dict: A dictionary, with Chain IDs as key assigned to lists of tuples (residue number, 3-letter-code). Sorted by residue number.
        None: if error occur while open the PDB file.
    """

    sequences = defaultdict(list)
    # to avoid duplicates per chain (atom vs. atom)
    seen_residues = defaultdict(set)

    try:
        with open(pdb_filepath, 'r') as pdbfile:
            for line in pdbfile:
                if line.startswith("ATOM"):
                    try:
                        # PDB format specifications:
                        # Atom Serial Number: 1-6 (not used)
                        # Atom Name:         13-16
                        # Alt Loc Indicator: 17
                        # Residue Name:      18-20 (Indices 17-19)
                        # Chain ID:          22    (Index 21)
                        # Residue Seq Num:   23-26 (Indices 22-25)
                        # Insertion Code:    27    (Index 26)

                        # only C-alpha atoms are considered, to avoid duplicates
                        res_name = line[17:20].strip()
                        chain_id = line[21].strip()

                        # some PDB files have whitespaces instead of Chain ID
                        if not chain_id:
                            # default: use chain A
                            chain_id = 'A'

                        res_seq_num_str = line[22:26].strip()

                        # only sequence number as integer
                        res_seq_num = int(res_seq_num_str)
                        # key for seen_residues
                        unique_res_id = res_seq_num

                        # add residue only once per chain
                        if unique_res_id not in seen_residues[chain_id]:
                            sequences[chain_id].append((res_seq_num, res_name))
                            seen_residues[chain_id].add(unique_res_id)

                    except (ValueError, IndexError) as e:
                        print(f"Warning: skip invalid or unexpected ATOM entries: {line.strip()} - Error: {e}", file=sys.stderr)
                        continue

    except FileNotFoundError:
        print(f"Error: Source file '{pdb_filepath}' not found.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error while reading PDB file '{pdb_filepath}': {e}", file=sys.stderr)
        return None

    # sort residues by sequence number
    for chain_id in sequences:
        sequences[chain_id].sort()

    return sequences

def format_sequence(sequences, code_format, output_style):
    """
    Format the extracted sequence by user options.

    Args:
        sequences (dict): from parse_pdb_sequence returned dictionary.
        code_format (str): 'one-letter' or 'three-letter'.
        output_style (str): 'single-line' or 'multi-line'.

    Returns:
        str: formatted sequence as string.
    """

    full_sequence_list = []
    unknown_residues = set()

    # Combine sequences of all chains (sorted by chain ID)
    for chain_id in sorted(sequences.keys()):
        chain_seq = [res_name for res_seq, res_name in sequences[chain_id]]
        full_sequence_list.extend(chain_seq)

    if not full_sequence_list:
        # empty sequence, if there are no entries
        return ""

    formatted_residues = []
    if code_format == 'one-letter':
        for res_name in full_sequence_list:
            # 'X' if unknown
            one_letter_code = THREE_TO_ONE.get(res_name, 'X')
            if one_letter_code == 'X' and res_name not in THREE_TO_ONE:
                unknown_residues.add(res_name)
            formatted_residues.append(one_letter_code)
        # no whitespaces between 1-letter-codes
        separator = ""
    else:
        # three-letter
        formatted_residues = full_sequence_list
        # whitespaces between 3-letter-codes
        separator = " "

    if unknown_residues:
        print(f"Warning: Unknown or non-standard-residue found and as 'X' represented (one-letter-code): {', '.join(sorted(list(unknown_residues)))}", file=sys.stderr)

    if output_style == 'single-line':
        # single-line
        return separator.join(formatted_residues)
    else:
        # multi-line
        return "\n".join(formatted_residues)

def write_output(target_filepath, content):
    """
    Writes the content in the target filepath.

    Args:
        target_filepath (str): Path to target file.
        content (str): content for target file.

    Returns:
        bool: True if success, False if error occurs.
    """

    try:
        with open(target_filepath, 'w') as outfile:
            outfile.write(content + "\n") # Füge am Ende einen Zeilenumbruch hinzu
        return True
    except IOError as e:
        print(f"Error: Can't find or write in target file '{target_filepath}': {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Unexpected error occured while writing into target file '{target_filepath}': {e}", file=sys.stderr)
        return False

def main():
    """
    Main function. Parses the arguments and calls the processing functions to write the sequence in the target file.
    """

    parser = argparse.ArgumentParser(
        description="Extract the protein sequences from PDB file and  write it in target file.",
        # shows standard values in help
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("source", help="Path to PDB source file.")
    parser.add_argument("target", help="Path to target file for sequence.")

    parser.add_argument(
        "--format",
        choices=['one-letter', 'three-letter'],
        default='one-letter',
        help="Output format of the amino acid codes."
    )

    parser.add_argument(
        "--output-style",
        choices=['single-line', 'multi-line'],
        default='single-line',
        help="Output style: 'single-line' (all in one line) or 'multi-line' (one code per line)."
    )

    args = parser.parse_args()

    print(f"Process PDB file: {args.source}")
    print(f"Output format: {args.format}, Output style: {args.output_style}")

    # 1. extract sequences
    sequences_data = parse_pdb_sequence(args.source)
    if sequences_data is None:
        # exit if error occurs
        sys.exit(1)

    if not sequences_data:
        print("Warning: No ATOM entries or no known amino acids in the PDB file.", file=sys.stderr)
        # create empty output file
        formatted_output = ""
    else:
        # 2. format sequences
        formatted_output = format_sequence(sequences_data, args.format, args.output_style)

    # 3. write sequences
    if write_output(args.target, formatted_output):
        print(f"Sequence written successfully in '{args.target}'-")
    else:
        # exit if error occurs
        sys.exit(1)

if __name__ == "__main__":
    main()