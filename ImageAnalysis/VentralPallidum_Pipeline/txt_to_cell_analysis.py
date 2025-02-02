import os
import pandas as pd

# Define all paths in a single dictionary (Windows-style)
paths = {
    "raw_detection": r"C:\Users\Jamie\Documents\BRAIN STUFF\VP_qp_LF - ITERATION4\detections_iteration4",
    "raw_annotation": r"C:\Users\Jamie\Documents\BRAIN STUFF\VP_qp_LF - ITERATION4\annotations_iteration4",
    "detection_csv": r"C:\Users\Jamie\Documents\BRAIN STUFF\VP_qp_LF - ITERATION4\detections_csv",
    "annotation_csv": r"C:\Users\Jamie\Documents\BRAIN STUFF\VP_qp_LF - ITERATION4\annotations_csv"
}

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":  # If not Windows (e.g., Linux or WSL)
        win_path = win_path.replace("\\", "/")  # Replace backslashes with forward slashes
        if win_path[1:3] == ":/":  # If it's a drive letter (e.g., C:/)
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"  # Convert to Unix path (e.g., /mnt/c/)
    return win_path

# Convert all paths to Unix-like if necessary
paths = {key: convert_to_unix_path(value) for key, value in paths.items()}

# Ensure the output directories exist
os.makedirs(paths["detection_csv"], exist_ok=True)
os.makedirs(paths["annotation_csv"], exist_ok=True)

# Function to convert text files to CSV
def convert_text_to_csv(input_path, output_path):
    print(f"Looking for files in: {input_path}")
    for file in os.listdir(input_path):
        if file.endswith(".txt"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, file.replace(".txt", ".csv"))
            try:
                # Assuming tab-delimited text files
                df = pd.read_csv(input_file, sep="\t")
                df.to_csv(output_file, index=False)
                print(f"Converted {file} to {output_file}")
            except Exception as e:
                print(f"Error converting {file}: {e}")

# Convert raw detection and annotation files
convert_text_to_csv(paths["raw_detection"], paths["detection_csv"])
convert_text_to_csv(paths["raw_annotation"], paths["annotation_csv"])

# Get all converted detection CSV files
filelist = [f for f in os.listdir(paths["detection_csv"]) if f.endswith(".csv")]

# Define Qupath colors and classifications
QPink = "AF488"  # QP Pink
QPBlue = "AF647"  # QP Blue

Pink_posName = "vglut2_Pos"
Pink_posName_2 = "vglut2_Pos: vgat_Neg"
Blue_posName = "vgat_Pos"
Blue_posName_2 = "vglut2_Neg: vgat_Pos"
double_positive = "vglut2_Pos: vgat_Pos"

# Initialize an empty dataframe with relevant columns
DataDraft = pd.DataFrame(columns=[
    "Sample", 
    "vglut2-: vgat+ Cell Density (cells/mm^2)", 
    "vglut2-: vgat+ Cell Count", 
    "vglut2-: vgat+ Cell Area (mm^2)", 
    "vglut2-: vgat+ Cell Percentage", 
    "vglut2-: vgat+ Intensity", 
    "vglut2+: vgat- Cell Density (cells/mm^2)", 
    "vglut2+: vgat- Cell Count", 
    "vglut2+: vgat- Cell Area (mm^2)", 
    "vglut2+: vgat- Cell Percentage", 
    "vglut2+: vgat- Intensity", 
    "Double Positive Cell Density (cells/mm^2)", 
    "Double Positive Cell Count", 
    "Double Positive Cell Area (mm^2)", 
    "Double Positive Cell Percentage", 
    "Total Cell Area (mm^2)", 
    "Total Annotation Area (mm^2)"
])

# Process each file
for k, file in enumerate(filelist):
    try:
        # Read detection and corresponding annotation data
        det_data = pd.read_csv(os.path.join(paths["detection_csv"], file))
        filename = file.replace(" Detections", "")
        ano_file = os.path.join(paths["annotation_csv"], filename)
        if not os.path.exists(ano_file):
            print(f"Annotation file {ano_file} not found for {file}. Skipping.")
            continue
        ano_data = pd.read_csv(ano_file)

        # Debug: Print the first few rows
        print(f"Processing {file}")
        print("Detection Data:")
        print(det_data.head())
        print("Annotation Data:")
        print(ano_data.head())

        # Subset data for specific cell populations
        QPpink_only = det_data[det_data['Classification'].isin([Pink_posName, Pink_posName_2])]
        QPblue_only = det_data[det_data['Classification'].isin([Blue_posName, Blue_posName_2])]
        QPboth = det_data[det_data['Classification'] == double_positive]

        # Calculate areas and statistics
        posPinkArea = QPpink_only['Cell: Area µm^2'].sum() / 1e6 if not QPpink_only.empty else 0
        posBlueArea = QPblue_only['Cell: Area µm^2'].sum() / 1e6 if not QPblue_only.empty else 0
        posBothArea = QPboth['Cell: Area µm^2'].sum() / 1e6 if not QPboth.empty else 0
        totalCellArea = posPinkArea + posBlueArea + posBothArea

        realAnnotations = ano_data[ano_data['Object type'].isin(["Annotation", "PathAnnotationObject"])]
        anoArea = realAnnotations['Area µm^2'].sum() / 1e6 if not realAnnotations.empty else 0

        pinkIntensity = QPpink_only['AF488: Cell: Mean'].mean() if not QPpink_only.empty else None
        blueIntensity = QPblue_only['AF647: Cell: Mean'].mean() if not QPblue_only.empty else None

        pinkCellCount = len(QPpink_only)
        blueCellCount = len(QPblue_only)
        bothCellCount = len(QPboth)
        totalCells = pinkCellCount + blueCellCount + bothCellCount

        pinkPercentage = (pinkCellCount / totalCells * 100) if totalCells > 0 else None
        bluePercentage = (blueCellCount / totalCells * 100) if totalCells > 0 else None
        bothPercentage = (bothCellCount / totalCells * 100) if totalCells > 0 else None

        # Populate DataDraft
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "vglut2-: vgat+ Cell Density (cells/mm^2)"] = (blueCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "vglut2-: vgat+ Cell Count"] = blueCellCount
        DataDraft.loc[k, "vglut2-: vgat+ Cell Area (mm^2)"] = posBlueArea
        DataDraft.loc[k, "vglut2-: vgat+ Cell Percentage"] = bluePercentage
        DataDraft.loc[k, "vglut2-: vgat+ Intensity"] = blueIntensity

        DataDraft.loc[k, "vglut2+: vgat- Cell Density (cells/mm^2)"] = (pinkCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "vglut2+: vgat- Cell Count"] = pinkCellCount
        DataDraft.loc[k, "vglut2+: vgat- Cell Area (mm^2)"] = posPinkArea
        DataDraft.loc[k, "vglut2+: vgat- Cell Percentage"] = pinkPercentage
        DataDraft.loc[k, "vglut2+: vgat- Intensity"] = pinkIntensity

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = (bothCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Positive Cell Count"] = bothCellCount
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea
        DataDraft.loc[k, "Double Positive Cell Percentage"] = bothPercentage

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea
        DataDraft.loc[k, "Total Annotation Area (mm^2)"] = anoArea

        print(f"Processed {file}")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Write the results to a CSV and XLSX file
DataDraft.to_csv("CHEESE_processed_data_with_percentages.csv", index=False)
DataDraft.to_excel("CHEESE_processed_data_with_percentages.xlsx", index=False)
