```bash
# Create a new Conda environment for bioinformatics
conda create --name bioinformatics python=3.10

# Activate the environment
conda activate bioinformatics

# Install essential bioinformatics libraries
conda install -c conda-forge biopython pandas numpy matplotlib
```

# *Setting Up VS Code*
1. Open **VS Code**.
2. Press **Cmd + Shift + P** (**Ctrl + Shift + P** on Windows/Linux).
3. Type **"Python: Select Interpreter"** and select it.
4. Choose the **bioinformatics Conda environment** (should look like:  
   ```
   .../anaconda3/envs/bioinformatics/bin/python
   ```



# Mutation Types
1. Single Nucleotide Polymorphisms (SNPs) (A → G, C → T, etc.)
2. Insertions (new nucleotides appear in the variant but not in the reference)
3. Deletions (nucleotides present in the reference are missing in the variant)
4. Amino Acid Changes (for mutations in coding regions)



# Reference paper:
https://pmc.ncbi.nlm.nih.gov/articles/PMC7387429/ 

