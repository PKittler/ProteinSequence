# ProteinSequence

ProteinSequence is a simple command-line tool to extract amino acid sequences from Protein Data Bank (PDB) files. It is written in Python 3 and allow the customization of the output format and layout.

## Features
- parses 'ATOM' records in PDB files to determine amino acid residues
- extract sequences from multiple chains
- sorts chains alphabetically by chain ID
- output formats: one-letter code and three-letter code
- output style: all codes on a single line or with each residue on a new line
- handles non-standard residues by representing them as 'X' in one-letter mode and prompts a warning
- pure Python, only standard libraries
- command-line interface for easy integration in other scripts

## Requirements

- Python 3.x

No external libraries are required.

## Installation

Save the script as Python file (e.g. 'proseq.py).

Linux / macOS: Make the script executable with
```bash
chmod +x proseq.py
```

## Usage
Run the script from your terminal, providing the input PDB file path and the desired output file path. Use options to control the output format.

**Basic Syntax:**
```bash
python proseq.py <source_pdb_file> <target_output_file> [options]
```

If it is executable on Linux / macOS:
```
./proseq.py <source_pdb_file> <target_output_file> [options]
```

## Examples
1. Extract sequence in one-letter-code, single line (default):
```
python proseq.py my_protein.pdb sequence_1l_single.txt
# Or: ./proseq.py my_protein.pdb sequence_1l_single.txt
```
2. Extract sequence in three-letter code, single line:
```
python proseq.py my_protein.pdb sequence_3l_single.txt --format three-letter
```
3. Extract sequence in one-letter code, multi-line (one residue per line):
```
python proseq.py complex.pdb sequence_1l_multi.seq --output-style multi-line
```
4. Extract sequence in three-letter code, multi-line:
```
python proseq.py complex.pdb sequence_3l_multi.seq --format three-letter --output-style multi-line
```
5. Show help message:
```
python proseq.py -h
# Or: ./proseq.py --help
```
## Command-Line Arguments
- source: (Positional argument) Path to the input PDB file
- target: (Positional argument) Path to the output file where the sequence will be written

## Options
- --format {one-letter, three-letter}:
  - Specifies the output format for amino acid codes
  - one-letter: Use single uppercase letters (e.g., A, R, N, ...), unknown/non-standard residues are represented as X 
  - three-letter: Use standard three-letter codes (e.g., ALA, ARG, ASN, ...), unknown/non-standard residues are included using their names from the PDB file
  - default: one-letter
- --output-style {single-line, multi-line}:
  - Specifies the layout of the output sequence
  - single-line: The entire sequence is written on a single line, three-letter codes will be space-separated
  - multi-line: Each amino acid residue is written on a new line
  - Default: single-line
- -h, --help:
  - Show the help message describing arguments and options, then exit

## Example Output Files
--format one-letter --output-style single-line (e.g., sequence_1l_single.txt):
> MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQRLQAAQATGENLAEVRAMSNDVTATVCAAFKESDGKPVSGAALQIAMMAQRHHTYATLMNKLGTIAKAALNNDQLARTTIFYQASAAVAEE

--format three-letter --output-style single-line (e.g., sequence_3l_single.txt)
> MET LYS THR ALA TYR ILE ALA LYS GLN ARG GLN ILE SER PHE VAL LYS SER HIS PHE SER ARG GLN LEU GLU GLU ARG LEU GLY LEU ILE GLU VAL GLN ALA PRO ILE LEU SER ARG VAL GLY ASP GLY THR GLN ASP ASN LEU SER GLY ALA GLU LYS ALA VAL GLN ARG LEU GLN ALA ALA GLN ALA THR GLY GLU ASN LEU ALA GLU VAL ARG ALA MET SER ASN ASP VAL THR ALA THR VAL CYS ALA ALA PHE LYS GLU SER ASP GLY LYS PRO VAL SER GLY ALA ALA LEU GLN ILE ALA MET MET ALA GLN ARG HIS HIS THR TYR ALA THR LEU MET ASN LYS LEU GLY THR ILE ALA LYS ALA ALA LEU ASN ASN ASP GLN LEU ALA ARG THR THR ILE PHE TYR GLN ALA SER ALA ALA VAL ALA GLU GLU

--format one-letter --output-style multi-line (e.g., sequence_1l_multi.seq)
> M
> 
> K
> 
> T
> 
> A
> 
> Y
> 
> I
> 
> A
> 
> K
>
> ...

--format three-letter --output-style multi-line (e.g., sequence_3l_multi.seq)
> MET
> 
> LYS
> 
> THR
> 
> ALA
> 
> TYR
> 
> ILE
> 
> ALA
> 
> LYS
> 
> ...

## Notes
The script performs basic parsing of ATOM records based on standard PDB column definitions. It may not correctly handle heavily modified or non-standard PDB formats. It identifies residues based on the first occurrence of a unique residue sequence number (resSeq) within each chain (chainID). It does not explicitly handle alternative locations (altLoc) or insertion codes (iCode) beyond using the resSeq integer for ordering and uniqueness within a chain.
Sequences from different chains in the PDB file are concatenated in alphabetical order of their chain IDs (e.g., chain A sequence followed by chain B sequence). Non-standard amino acids or other molecules listed in ATOM records might be included as 'X' (one-letter) or their PDB name (three-letter) if they occupy a position in the residue sequence. A warning message will be printed to stderr if unknown residue types are encountered when converting to one-letter codes.

## License
This project is provided under the GNU License. Read the license file for further information.

