# Coding Projects

## General Applications

### Budget Buddy App

#### Overview
Budget Buddy is an interactive budgeting tool created with Streamlit and Plotly. It helps users track monthly income, expenses, and visualize their budget allocations.

[Live App](https://jam14d-projects-budgetbuddyapp-tnngqb.streamlit.app/)

#### Features
- **Interactive Sidebar**: Input monthly income, edit pre-filled common expenses, and add custom categories.
- **Real-Time Budget Calculations**: Instantly updates total expenses and remaining balance.
- **Expense Breakdown**: Detailed views per category.
- **Visualization**: Interactive pie chart showing expense distribution.
- **Responsive Design**: Enhanced aesthetics via customized CSS.

#### How to Use
1. **Set Monthly Income**
2. **Adjust Expenses**
3. **Add Custom Categories**
4. **Review Budget Summary**
5. **Visualize Expenses**

#### Requirements
- Python
- Streamlit (`pip install streamlit`)
- Plotly (`pip install plotly`)

#### Running the App
```bash
streamlit run app.py
```

---

## Scientific Computing

### Brain Tumor Classification using MRI Scans

#### Overview
Classify MRI scans into:
- **Glioma**
- **Meningioma**
- **Pituitary Tumor**
- **No Tumor (Healthy Brain)**

#### Setup Instructions
- Clone repository or download project files.
- Create and activate a Python virtual environment:
```bash
python3.10 -m venv brain_tumor_env
source brain_tumor_env/bin/activate
```
- Upgrade pip:
```bash
pip install --upgrade pip
```
- Install dependencies:
```bash
pip install scikit-learn seaborn matplotlib tensorflow-macos keras tensorboard tensorflow-estimator tensorflow-metal
```
- Organize dataset from [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset).
- Split dataset using provided Python script:
```bash
python split_train_val.py
```

#### Project Goals
- Image preprocessing and visualization
- CNN training
- Data augmentation
- Model evaluation (accuracy, loss, confusion matrix)
- Save trained models

#### Using VGG16 Model
- Pre-trained on ImageNet.
- Feature extraction and transfer learning.

---

### COVID-19 Variant Analysis: Omicron (BA.3.1) vs. Reference Genome

#### Overview
Analyze genetic variations between Omicron (BA.3.1) and reference SARS-CoV-2 genome.

#### Data
- Reference Genome: `NC_045512.fasta`
- Omicron Variant Genome: `BA.3.1.fasta`

#### Key Functionalities
- Sequence loading and comparison
- SNP detection and classification
  - Transitions (A <-> G, C <-> T)
  - Transversions (other substitutions)
- Data Visualization (histogram, pie chart)

#### Results
- SNP totals and distribution
- Transitions/transversions ratio

---

### Puncta Intensity Analysis

#### Overview
Automated analysis pipeline for whole-slide image data focusing on intensity and puncta detection.

#### Key Features
- Automated data filtering (outlier removal)
- Adaptive thresholding
- Statistical comparative analysis
- Visualization (publication-ready plots)

---

