from Bio import SeqIO
from Bio.Seq import Seq

# Load reference genome
ref_file = "/Users/jamieannemortel/Projects/Bioinformatics/covid_analysis/data/reference-NC_045512.fasta"
#testing
# Load variant (an omnicron)
variant_file = "/Users/jamieannemortel/Projects/Bioinformatics/covid_analysis/data/BA.3.1.fasta"

def load_fasta(filename):
    record = SeqIO.read(filename, "fasta")
    return str(record.seq)

# Load sequences
reference_seq = load_fasta(ref_file)
variant_seq = load_fasta(variant_file)

print(f"Reference Genome Length: {len(reference_seq)}")
print(f"Variant Genome Length: {len(variant_seq)}")
