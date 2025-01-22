import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

##SPECIFIC TO VGAT2: OPRM1 COMPOSITE
##IN PROGRESS!


# Define all paths in a single dictionary (Windows-style)
paths = {
    "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    "raw_annotation": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/annotations_iteration4_vgatwithMu_12.13.24",
    "detection_csv": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24_CSV",
    "annotation_csv": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/annotations_iteration4_vgatwithMu_12.13.24_CSV"
}

# Define directories for saving pie charts
base_dir = "/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE"
per_image_dir = os.path.join(base_dir, "PieCharts_Per_Image")
aggregated_dir = os.path.join(base_dir, "PieChart_Aggregated")

# Ensure the directories exist
os.makedirs(per_image_dir, exist_ok=True)
os.makedirs(aggregated_dir, exist_ok=True)

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":
        win_path = win_path.replace("\\", "/")
        if win_path[1:3] == ":/":
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"
    return win_path

# Convert all paths to Unix-like if necessary
paths = {key: convert_to_unix_path(value) for key, value in paths.items()}

# Ensure the output directories exist
os.makedirs(paths["detection_csv"], exist_ok=True)
os.makedirs(paths["annotation_csv"], exist_ok=True)

# Function to convert text files to CSV
def convert_text_to_csv(input_path, output_path):
    for file in os.listdir(input_path):
        if file.endswith(".txt"):
            input_file = os.path.join(input_path, file)
            output_file = os.path.join(output_path, file.replace(".txt", ".csv"))
            try:
                df = pd.read_csv(input_file, sep="\t")
                df.to_csv(output_file, index=False)
            except Exception as e:
                print(f"Error converting {file}: {e}")

# Convert raw detection and annotation files
convert_text_to_csv(paths["raw_detection"], paths["detection_csv"])
convert_text_to_csv(paths["raw_annotation"], paths["annotation_csv"])

# Get all converted detection CSV files
filelist = [f for f in os.listdir(paths["detection_csv"]) if f.endswith(".csv")]

# Define VGAT colors and classifications
Yellow_posName = "oprm1_Pos"
Yellow_posName_2 = "vgat_Neg: oprm1_Pos"
Blue_posName = "vgat_Pos"
Blue_posName_2 = "vgat_Pos: oprm1_Neg"
double_positive = "vgat_Pos: oprm1_Pos"
double_negative = "vgat_Neg: oprm1_Neg"

# Additional subcellular metric columns
subcellular_metrics = [
    "Subcellular cluster: Channel 2: Area",
    "Subcellular cluster: Channel 2: Mean channel intensity",
    "Subcellular: Channel 2: Num spots estimated",
    "Subcellular: Channel 2: Num single spots",
    "Subcellular: Channel 2: Num clusters"
]

# Initialize an empty dataframe with relevant columns
DataDraft = pd.DataFrame(columns=[
    "Sample",
    "oprm1-: vgat+ Cell Density (cells/mm^2)",
    "oprm1-: vgat+ Cell Count",
    "oprm1-: vgat+ Cell Area (mm^2)",
    "oprm1-: vgat+ Cell Percentage",
    "oprm1-: vgat+ Intensity",
    "oprm1+: vgat- Cell Density (cells/mm^2)",
    "oprm1+: vgat- Cell Count",
    "oprm1+: vgat- Cell Area (mm^2)",
    "oprm1+: vgat- Cell Percentage",
    "oprm1+: vgat- Intensity",
    "Double Positive Cell Density (cells/mm^2)",
    "Double Positive Cell Count",
    "Double Positive Cell Area (mm^2)",
    "Double Positive Cell Percentage",
    "Double Negative Cell Density (cells/mm^2)",
    "Double Negative Cell Count",
    "Double Negative Cell Area (mm^2)",
    "Double Negative Cell Percentage",
    "Total Cell Area (mm^2)",
    "Total Annotation Area (mm^2)"
] + [f"{metric} ({cls})" for metric in subcellular_metrics for cls in [Yellow_posName_2, Blue_posName_2, double_positive]])

# Process each file
for k, file in enumerate(filelist):
    try:
        det_data = pd.read_csv(os.path.join(paths["detection_csv"], file))
        filename = file.replace(" Detections", "")
        ano_file = os.path.join(paths["annotation_csv"], filename)
        if not os.path.exists(ano_file):
            continue
        ano_data = pd.read_csv(ano_file)

        # Subset data for specific cell populations
        Yellow_only = det_data[det_data['Classification'].isin([Yellow_posName, Yellow_posName_2])]
        Blue_only = det_data[det_data['Classification'].isin([Blue_posName, Blue_posName_2])]
        Both = det_data[det_data['Classification'] == double_positive]
        None_cells = det_data[det_data['Classification'] == double_negative]

        # Calculate areas and statistics
        posYellowArea = Yellow_only['Cell: Area µm^2'].sum() / 1e6 if not Yellow_only.empty else 0
        posBlueArea = Blue_only['Cell: Area µm^2'].sum() / 1e6 if not Blue_only.empty else 0
        posBothArea = Both['Cell: Area µm^2'].sum() / 1e6 if not Both.empty else 0
        posNoneArea = None_cells['Cell: Area µm^2'].sum() / 1e6 if not None_cells.empty else 0
        totalCellArea = posYellowArea + posBlueArea + posBothArea

        realAnnotations = ano_data[ano_data['Object type'].isin(["Annotation", "PathAnnotationObject"])]
        anoArea = realAnnotations['Area µm^2'].sum() / 1e6 if not realAnnotations.empty else 0

        YellowIntensity = Yellow_only['AF568: Cell: Mean'].mean() if not Yellow_only.empty else None
        BlueIntensity = Blue_only['AF647: Cell: Mean'].mean() if not Blue_only.empty else None

        YellowCellCount = len(Yellow_only)
        BlueCellCount = len(Blue_only)
        bothCellCount = len(Both)
        noneCellCount = len(None_cells)
        totalCells = YellowCellCount + BlueCellCount + bothCellCount + noneCellCount

        YellowPercentage = (YellowCellCount / totalCells * 100) if totalCells > 0 else None
        BluePercentage = (BlueCellCount / totalCells * 100) if totalCells > 0 else None
        bothPercentage = (bothCellCount / totalCells * 100) if totalCells > 0 else None
        nonePercentage = (noneCellCount / totalCells * 100) if totalCells > 0 else None

        # Populate DataDraft
        DataDraft.loc[k, "Sample"] = filename
        DataDraft.loc[k, "oprm1-: vgat+ Cell Density (cells/mm^2)"] = (BlueCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "oprm1-: vgat+ Cell Count"] = BlueCellCount
        DataDraft.loc[k, "oprm1-: vgat+ Cell Area (mm^2)"] = posBlueArea
        DataDraft.loc[k, "oprm1-: vgat+ Cell Percentage"] = BluePercentage
        DataDraft.loc[k, "oprm1-: vgat+ Intensity"] = BlueIntensity

        DataDraft.loc[k, "oprm1+: vgat- Cell Density (cells/mm^2)"] = (YellowCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "oprm1+: vgat- Cell Count"] = YellowCellCount
        DataDraft.loc[k, "oprm1+: vgat- Cell Area (mm^2)"] = posYellowArea
        DataDraft.loc[k, "oprm1+: vgat- Cell Percentage"] = YellowPercentage
        DataDraft.loc[k, "oprm1+: vgat- Intensity"] = YellowIntensity

        DataDraft.loc[k, "Double Positive Cell Density (cells/mm^2)"] = (bothCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Positive Cell Count"] = bothCellCount
        DataDraft.loc[k, "Double Positive Cell Area (mm^2)"] = posBothArea
        DataDraft.loc[k, "Double Positive Cell Percentage"] = bothPercentage

        DataDraft.loc[k, "Double Negative Cell Density (cells/mm^2)"] = (noneCellCount / totalCellArea) if totalCellArea > 0 else None
        DataDraft.loc[k, "Double Negative Cell Count"] = noneCellCount
        DataDraft.loc[k, "Double Negative Cell Area (mm^2)"] = posNoneArea
        DataDraft.loc[k, "Double Negative Cell Percentage"] = nonePercentage

        DataDraft.loc[k, "Total Cell Area (mm^2)"] = totalCellArea
        DataDraft.loc[k, "Total Cell Count"] = totalCells
        DataDraft.loc[k, "Total Annotation Area (mm^2)"] = anoArea

        # Subcellular metrics
        for cls in [Yellow_posName_2, Blue_posName_2, double_positive, double_negative]:
            cls_data = det_data[det_data['Classification'] == cls]
            for metric in subcellular_metrics:
                DataDraft.loc[k, f"{metric} ({cls})"] = cls_data[metric].sum() if metric in cls_data.columns else None

    except Exception as e:
        print(f"Error processing {file}: {e}")

#commenting out pie chart, need to fix
# # Define custom pastel colors
# custom_colors = ["#CBC3E3", "#80D8FF"]  # Orange-yellow and light blue
# legend_labels = ["VGAT+: OPRM1+", "VGAT+: OPRM1-"]

# # Generate pie chart for each image
# for idx, row in DataDraft.iterrows():
#     sample = row["Sample"]
#     double_positive = row["Double Positive Cell Count"]
#     vgat_only = row["oprm1-: vgat+ Cell Count"]

#     if pd.isna(double_positive) or pd.isna(vgat_only):
#         continue

#     fig = plt.figure(figsize=(8, 8))
#     plt.pie(
#         [double_positive, vgat_only],
#         autopct="%1.1f%%",
#         startangle=90,
#         colors=custom_colors,
#         wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
#     )
#     #plt.title(f"Proportion of OPRM1+ to VGAT+ Cells for {sample}")
#     plt.axis("equal")

#     file_path = os.path.join(per_image_dir, f"{sample}_PieChart.png")
#     plt.savefig(file_path, bbox_inches="tight")
#     plt.close(fig)

# # Aggregated pie chart
# aggregated_file_path = os.path.join(aggregated_dir, "Aggregated_PieChart.png")
# plt.pie(
#     [DataDraft["Double Positive Cell Count"].sum(), DataDraft["oprm1-: vgat+ Cell Count"].sum()],
#     autopct="%1.1f%%",
#     startangle=90,
#     colors=custom_colors,
#     wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},
# )
# #plt.title("Proportion of OPRM1+ to VGAT+ Cells (Aggregated)")
# plt.axis("equal")
# plt.savefig(aggregated_file_path, bbox_inches="tight")
# plt.close()

# Write the results to CSV and XLSX
DataDraft.to_csv("vgat_oprm1_subcellular_metrics.csv", index=False)
DataDraft.to_excel("vgat_oprm1_subcellular_metrics.xlsx", index=False)
