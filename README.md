# 🧠 Brain Tumor Classification using MRI Scans

## Overview
This project aims to classify brain MRI scans into four categories:

1. **Glioma**
2. **Meningioma**
3. **Pituitary Tumor**
4. **No Tumor (Healthy Brain)**

---

## Setup Instructions
### 1. Clone or Download the Project
```bash
git clone https://github.com/your-repo/brain-tumor-classification.git
cd brain-tumor-classification
```
Otherwise, download and extract the project folder.

### 2. Create and Activate a Virtual Environment

Navigate to the project folder:
```bash
cd ~/Documents/brain_tumor_project
```
Create a virtual environment named `brain_tumor_env`:
```bash
python3.10 -m venv brain_tumor_env
```
Activate the environment:
```bash
source brain_tumor_env/bin/activate  # Mac/Linux
```
For Windows:
```bash
brain_tumor_env\Scripts\activate
```

### 3. Upgrade pip
```bash
pip install --upgrade pip
```

### 4. Install Dependencies
```bash
pip install scikit-learn seaborn matplotlib tensorflow-macos keras tensorboard tensorflow-estimator tensorflow-metal
```

### 5. Download and Organize the Dataset

Download the dataset from Kaggle: [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)

Extract the dataset and organize it as follows:
```bash
brain_tumor_dataset/
├── train/
│   ├── glioma/
│   ├── meningioma/
│   ├── pituitary/
│   ├── no_tumor/
├── val/  # (Create this manually and move 20% of train images here)
│   ├── glioma/
│   ├── meningioma/
│   ├── pituitary/
│   ├── no_tumor/
├── test/
│   ├── glioma/
│   ├── meningioma/
│   ├── pituitary/
│   ├── no_tumor/
```
Use the provided Python script to split the training set into validation:
```bash
python split_train_val.py
```

---

## Project Goals
- Preprocess and visualize MRI scan images.
- Train a CNN model to classify brain tumors.
- Implement data augmentation to improve performance.
- Evaluate the model using accuracy, loss, and confusion matrix.
- Save the trained model for future predictions.

## Using pre-trained model VGG16
- Pre-trained CNN developed by Oxford’s Visual Geometry Group.
- Trained on ImageNet for object recognition.
- Deep architecture with 16 layers (13 convolutional + 3 dense).
- For feature extraction and transfer learning.

---

# 🦠 COVID-19 Variant Analysis: Omicron (BA.3.1) vs. Reference Genome

## Overview
This project analyzes genetic variations between the **Omicron (BA.3.1) variant** and the **reference SARS-CoV-2 genome (NC_045512)**. It identifies **single nucleotide polymorphisms (SNPs)**, classifies them into **transitions and transversions**, and visualizes their distribution.

## Data
- **Reference Genome**: `NC_045512.fasta`
- **Omicron Variant Genome**: `BA.3.1.fasta`

## Key Functionalities
1. **Load and Compare Sequences**: Extracts sequences from FASTA files and compares the Omicron variant against the reference genome.
2. **SNP Detection**: Identifies positions where nucleotide changes occur.
3. **SNP Classification**:
   - *Transitions*: A <-> G or C <-> T (purine ↔ purine, pyrimidine ↔ pyrimidine changes)
   - *Transversions*: Other nucleotide substitutions (purine ↔ pyrimidine changes)
4. **Data Visualization**:
   - Histogram showing SNP distribution across the genome.
   - Pie chart comparing the proportion of transitions vs. transversions.

## Results
- Total number of SNPs detected
- Distribution of SNPs across the genome
- Ratio of transitions to transversions

---

# Puncta Intensity Analysis

## Overview
This pipeline automates the **processing, filtering, and statistical analysis** of whole-slide image data, focusing on **intensity and puncta detection**. It applies **outlier removal** and **adaptive thresholding** to extract meaningful insights.

## Key Features
- **Automated data filtering**: Removes extreme values to improve statistical reliability.
- **Threshold optimization**: Dynamically identifies intensity cutoffs for feature detection.
- **Comparative analysis**: Assesses differences between experimental groups using statistical tests.
- **Data visualization**: Generates **publication-ready** plots.

---
