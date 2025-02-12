

from Bio.Seq import Seq

dna = Seq("ATGCGTACGTAGCTAGCTAG")
print("Reverse Complement:", dna.reverse_complement())
print("mRNA:", dna.transcribe())
print("Protein:", dna.translate())

