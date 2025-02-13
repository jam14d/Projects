import matplotlib.pyplot as plt
import numpy as np
from Bio import SeqIO
from Bio.Seq import Seq

# Load reference genome
ref_file = "/Users/jamieannemortel/Projects/Bioinformatics/covid_analysis_project/data/reference-NC_045512.fasta"

# Load variant (an omnicron)
variant_file = "/Users/jamieannemortel/Projects/Bioinformatics/covid_analysis_project/data/BA.3.1.fasta"

def load_fasta(filename):
    record = SeqIO.read(filename, "fasta")
    return str(record.seq)

# Load sequences
reference_seq = load_fasta(ref_file)
variant_seq = load_fasta(variant_file)

#Find Genome Length 
print(f"Reference Genome Length: {len(reference_seq)}")
print(f"Variant Genome Length: {len(variant_seq)}")

def find_snps(ref_seq, var_seq):
    """
    Identifies SNPs (Single Nucleotide Polymorphisms) by comparing two sequences.

    Args:
        ref_seq (str): The reference genome sequence.
        var_seq (str): The variant genome sequence.

    Returns:
        list: A list of SNPs, where each entry is a tuple (position, ref_nucleotide, var_nucleotide).
    """
    snps = []  # Store SNPs as (position, reference nucleotide, variant nucleotide)

    for i, (ref_nuc, var_nuc) in enumerate(zip(ref_seq, var_seq)):  # Loop through both sequences
        if ref_nuc != var_nuc:  # If nucleotides don't match, it's a SNP
            snps.append((i, ref_nuc, var_nuc))  # Store the SNP

    return snps  # Return list of SNPs

# Find SNPs in the genome
snps = find_snps(reference_seq, variant_seq)

# Print a summary of the findings
print(f"Total SNPs Found: {len(snps)}")  # Print the total number of SNPs detected
print("First 10 SNPs:", snps[:10])  # Print the first 10 SNPs to check the output


# Extract SNP positions from the list of SNPs
snp_positions = [pos for pos, _, _ in snps]  

# Create a histogram of SNP positions
# plt.figure(figsize=(12, 5))  # Set figure size
# plt.hist(snp_positions, bins=50, color='purple', alpha=0.7)  # Plot histogram with 50 bins
# plt.xlabel("Genome Position")  # Label x-axis
# plt.ylabel("SNP Frequency")  # Label y-axis
# plt.title("Distribution of SNPs Across the Genome")  # Set plot title
# plt.show()  # Display the histogram


def classify_snp_types(snps):
    """
    Classifies SNPs into transitions and transversions.

    Args:
        snps (list): List of SNPs in the format (position, reference nucleotide, variant nucleotide).

    Returns:
        dict: A dictionary with the counts of transitions and transversions.
    """
    # Define transition and transversion rules
    transitions = {"A": "G", "G": "A", "C": "T", "T": "C"}  # Purine ↔ Purine and Pyrimidine ↔ Pyrimidine
    transversions = {"A": ["C", "T"], "G": ["C", "T"], "C": ["A", "G"], "T": ["A", "G"]}  # Purine ↔ Pyrimidine

    # Initialize counts
    counts = {"Transitions": 0, "Transversions": 0}

    for _, ref_nuc, var_nuc in snps:  # Loop through all SNPs
        if transitions.get(ref_nuc) == var_nuc:  # If change follows transition rule
            counts["Transitions"] += 1
        elif var_nuc in transversions.get(ref_nuc, []):  # If change follows transversion rule
            counts["Transversions"] += 1

    return counts  # Return count of transitions and transversions

# Classify SNPs into transitions vs. transversions
snp_classification = classify_snp_types(snps)

# Print results
print(f"Transitions: {snp_classification['Transitions']}")
print(f"Transversions: {snp_classification['Transversions']}")

plt.figure(figsize=(6,6))  # Set figure size
plt.pie(
    snp_classification.values(),  # Use transition/transversion counts
    labels=snp_classification.keys(),  # Label the pie chart sections
    autopct='%1.1f%%',  # Display percentages
    colors=['blue', 'orange']  # Set colors for better visualization
)
plt.title("Comparison of SNP Types: Omicron (BA.3.1) vs. SARS-CoV-2 Reference")  # Title for the chart
plt.show()  # Display the pie chart
