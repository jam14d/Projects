# Projects Repository

# *COVID-19 Variant Analysis: Omicron (BA.3.1) vs. Reference Genome*

## Overview
This project analyzes genetic variations between the Omicron (BA.3.1) variant and the reference SARS-CoV-2 genome (NC_045512). It specifically identifies single nucleotide polymorphisms (SNPs), classifies them into transitions and transversions, and visualizes their distribution across the genome.

## Data
- **Reference Genome**: `NC_045512.fasta`
- **Omicron Variant Genome**: `BA.3.1.fasta`

## Key Functionalities
1. **Load and Compare Sequences**: Extracts sequences from FASTA files and compares the Omicron variant against the reference genome.
2. **SNP Detection**: Identifies positions where nucleotide changes occur.
3. **SNP Classification**: Categorizes SNPs into:
   - *Transitions*: A <-> G or C <-> T (purine ↔ purine, pyrimidine ↔ pyrimidine changes)
   - *Transversions*: Other nucleotide substitutions (purine ↔ pyrimidine changes)
4. **Data Visualization**:
   - Histogram showing SNP distribution across the genome.
   - Pie chart comparing the proportion of transitions vs. transversions.

## Results
- Total number of SNPs detected
- Distribution of SNPs across the genome
- Ratio of transitions to transversions

# *Image Analysis*

## Overview
This folder contains a pipeline that automates the **processing, filtering, and statistical analysis** of whole-slide image data, focusing on **intensity and puncta detection**. It applies **outlier removal** and **adaptive thresholding** to refine raw data and extract meaningful insights. The goal is to ensure **robust quantification** while reducing noise and variability in biological image datasets.

## Key Applications
- **Automated data filtering**: Removes extreme values to improve statistical reliability.
- **Threshold optimization**: Dynamically identifies intensity cutoffs for feature detection.
- **Comparative analysis**: Assesses differences between experimental groups using statistical tests.
- **Data visualization**: Generates **publication-ready** plots for reporting findings.

## Features
- Loads **raw detection data** from whole-slide image analysis.
- Identifies and removes **outliers** using an adaptive statistical approach.
- Computes an **intensity threshold** for feature segmentation.
- Performs **non-parametric statistical comparisons** to detect significant differences.
- Saves **visualization plots** for easier interpretation of results.


# *Code to Codons*

## Overview
A Streamlit web application that simulates the conversion of text to DNA, applies mutations, and translates the DNA through RNA into protein sequences.

### Features
- Convert text to DNA sequence.
- Mutate DNA and transcribe into RNA.
- Translate RNA to protein and highlight stop codons.

### Installation
1. Clone the repo and navigate into the specific project directory.
2. Create a virtual environment and install dependencies.
3. Run the app with `streamlit run app.py`.

### Usage
Input text to convert and mutate into DNA, view the RNA transcription, and the resulting protein sequence with highlighted stop codons.

### Modules
Includes modules for DNA conversion, mutation, RNA transcription, and protein translation.
