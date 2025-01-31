import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu

# Define paths for VGAT and VGLUT2 data
paths = {
    "vgat_positive_oprm1_positive": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    "vglut2_positive_oprm1_positive": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24",
}

# Create a "plots" directory
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots")
os.makedirs(plots_dir, exist_ok=True)

# Define classifications and parent values
classifications = {
    "vgat_positive_oprm1_positive": ["vgat_Pos: oprm1_Pos"],
    "vglut2_positive_oprm1_positive": ["vglut2_Pos: oprm1_Pos"],
}
parent_values = {
    "vgat_positive_oprm1_positive": "Cell (vgat_Pos: oprm1_Pos)",
    "vglut2_positive_oprm1_positive": "Cell (vglut2_Pos: oprm1_Pos)",
}

# Initialize a dictionary to collect data for each classification
data = {key: pd.DataFrame() for key in classifications.keys()}

# Helper function to read data
def read_data(file_path):
    try:
        return pd.read_csv(file_path, sep="\t", encoding="utf-8")
    except UnicodeDecodeError:
        print(f"Error reading file {file_path}: Unable to decode.")
        return None

# Helper function to detect and remove outliers using the IQR method
def remove_outliers(df, column):
    if df.empty:
        return df
    Q1 = df[column].quantile(0.25)  # First quartile (25th percentile)
    Q3 = df[column].quantile(0.75)  # Third quartile (75th percentile)
    IQR = Q3 - Q1  # Interquartile range
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Collect intensity data
def collect_intensity_data(raw_detection_path, labels):
    filelist = [f for f in os.listdir(raw_detection_path) if f.endswith(".txt")]

    intensity_data = []
    for file in filelist:
        file_path = os.path.join(raw_detection_path, file)
        det_data = read_data(file_path)
        if det_data is None or "Classification" not in det_data.columns or "AF568: Cell: Mean" not in det_data.columns:
            print(f"Skipping file {file}: Required columns for intensity are missing.")
            continue

        filtered_data = det_data[det_data["Classification"].isin(labels)]
        intensity_data.append(filtered_data[["AF568: Cell: Mean"]].dropna())

    if intensity_data:
        return pd.concat(intensity_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=["AF568: Cell: Mean"])

# Collect puncta data
def collect_puncta_data(raw_detection_path, parent_value):
    filelist = [f for f in os.listdir(raw_detection_path) if f.endswith(".txt")]

    puncta_data = []
    for file in filelist:
        file_path = os.path.join(raw_detection_path, file)
        det_data = read_data(file_path)
        if det_data is None or "Parent" not in det_data.columns or "Num spots" not in det_data.columns:
            print(f"Skipping file {file}: Required columns for puncta are missing.")
            continue

        filtered_data = det_data[det_data["Parent"] == parent_value]
        puncta_data.append(filtered_data[["Num spots"]].dropna())

    if puncta_data:
        return pd.concat(puncta_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=["Num spots"])

# Collect data for each classification
for key in classifications.keys():
    raw_detection_path = paths[key]
    intensity_df = collect_intensity_data(raw_detection_path, classifications[key])
    puncta_df = collect_puncta_data(raw_detection_path, parent_values[key])

    if not intensity_df.empty and not puncta_df.empty:
        merged_data = pd.concat([intensity_df, puncta_df], axis=1)
        data[key] = merged_data.dropna()
    else:
        print(f"No data for classification: {key}")

# File to save statistics
stats_file_path = os.path.join(plots_dir, "vgat_vs_vglut2_stats.txt")
with open(stats_file_path, "w") as stats_file:
    stats_file.write("VGAT vs VGLUT2 Statistical Comparison\n")
    stats_file.write("=" * 50 + "\n\n")

    # Compare VGAT vs VGLUT2 for intensity
    vgat_intensity = data["vgat_positive_oprm1_positive"]["AF568: Cell: Mean"]
    vglut2_intensity = data["vglut2_positive_oprm1_positive"]["AF568: Cell: Mean"]
    
    if not vgat_intensity.empty and not vglut2_intensity.empty:
        intensity_stats = mannwhitneyu(vgat_intensity, vglut2_intensity, alternative="two-sided")
        stats_file.write(f"Intensity Comparison:\n")
        stats_file.write(f"  U-statistic: {intensity_stats.statistic}, p-value: {intensity_stats.pvalue}\n\n")

    # Compare VGAT vs VGLUT2 for puncta
    vgat_puncta = data["vgat_positive_oprm1_positive"]["Num spots"]
    vglut2_puncta = data["vglut2_positive_oprm1_positive"]["Num spots"]

    if not vgat_puncta.empty and not vglut2_puncta.empty:
        puncta_stats = mannwhitneyu(vgat_puncta, vglut2_puncta, alternative="two-sided")
        stats_file.write(f"Puncta Comparison:\n")
        stats_file.write(f"  U-statistic: {puncta_stats.statistic}, p-value: {puncta_stats.pvalue}\n\n")

    # # Write subpopulation statistics for each classification

    # for key, df in data.items():
    #     if not df.empty:
    #         stats_file.write(f"Statistics for {key.replace('_', ' ').title()}\n")
    #         stats_file.write(f"Total Cells: {len(df)}\n")

    #         df["Subpopulation"] = pd.cut(
    #             df["AF568: Cell: Mean"],
    #             bins=[-float("inf"), 120, float("inf")],
    #             labels=["Low Intensity", "High Intensity"]
    #         ).astype(str) + " | " + pd.cut(
    #             df["Num spots"],
    #             bins=[-float("inf"), 2, float("inf")],
    #             labels=["Low Puncta", "High Puncta"]
    #         ).astype(str)

    #         subpop_counts = df["Subpopulation"].value_counts()
    #         for subpop, count in subpop_counts.items():
    #             stats_file.write(f"  {subpop}: {count}\n")

    #         stats_file.write("\n")
    
# Define a mapping of internal names to display names
cell_type_rename = {
    "vgat_positive_oprm1_positive": "VGAT+: OPRM1+",
    "vglut2_positive_oprm1_positive": "VGLUT2+: OPRM1+"
}

# ------------------------ Descriptive Statistics ------------------------
descriptive_stats_path = os.path.join(plots_dir, "descriptive_statistics.txt")

with open(descriptive_stats_path, "w") as stats_file:
    stats_file.write("Descriptive Statistics for VGAT and VGLUT2\n")
    stats_file.write("=" * 50 + "\n\n")

    for key, df in data.items():
        if not df.empty:
            stats_file.write(f"Descriptive Stats for {cell_type_rename[key]}:\n")
            
            # Compute descriptive statistics
            intensity_desc = df["AF568: Cell: Mean"].describe()
            puncta_desc = df["Num spots"].describe()
            
            stats_file.write("Intensity (AF568: Cell: Mean):\n")
            stats_file.write(f"  Mean: {intensity_desc['mean']:.2f}, Median: {intensity_desc['50%']:.2f}\n")
            stats_file.write(f"  Std: {intensity_desc['std']:.2f}, Min: {intensity_desc['min']:.2f}, Max: {intensity_desc['max']:.2f}\n")
            stats_file.write(f"  Q1: {intensity_desc['25%']:.2f}, Q3: {intensity_desc['75%']:.2f}\n\n")

            stats_file.write("Puncta (Num spots):\n")
            stats_file.write(f"  Mean: {puncta_desc['mean']:.2f}, Median: {puncta_desc['50%']:.2f}\n")
            stats_file.write(f"  Std: {puncta_desc['std']:.2f}, Min: {puncta_desc['min']:.2f}, Max: {puncta_desc['max']:.2f}\n")
            stats_file.write(f"  Q1: {puncta_desc['25%']:.2f}, Q3: {puncta_desc['75%']:.2f}\n\n")
            stats_file.write("-" * 50 + "\n")


#Visualization
subpop_comparison = []
for cell_type, df in data.items():
    if not df.empty:
        subpop_comparison.extend([
            {"Cell Type": cell_type, "Intensity": row["AF568: Cell: Mean"], "Puncta": row["Num spots"]}
            for _, row in df.iterrows()
        ])


if subpop_comparison:
    subpop_comparison_df = pd.DataFrame(subpop_comparison)

    # Apply renaming correctly
    subpop_comparison_df["Cell Type"] = subpop_comparison_df["Cell Type"].map(cell_type_rename)

    # Apply filtering: Only include points with Puncta > 2 and Intensity > 120
    filtered_df = subpop_comparison_df[
        (subpop_comparison_df["Puncta"] > 2) & (subpop_comparison_df["Intensity"] > 120)
    ]

    # Dynamically determine thresholds using the median of the dataset
    intensity_threshold = filtered_df["Intensity"].median()
    puncta_threshold = filtered_df["Puncta"].median()

    # Apply dynamic binning
    filtered_df["Subpopulation"] = pd.cut(
        filtered_df["Intensity"],
        bins=[-float("inf"), intensity_threshold, float("inf")],
        labels=["Low Intensity", "High Intensity"]
    ).astype(str) + " | " + pd.cut(
        filtered_df["Puncta"],
        bins=[-float("inf"), puncta_threshold, float("inf")],
        labels=["Low Puncta", "High Puncta"]
    ).astype(str)

    # Ensure we still have valid data
    if not filtered_df.empty:

        # **PLOT1: Subpopulation Analysis (colored by Subpopulation Class)**
        ##WANT THIS TO EVENTUALLY BIN BY LOW VS. HIGH DYNAMICALLY
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            data=filtered_df,
            x="Intensity",
            y="Puncta",
            hue="Subpopulation",
            palette="vlag",  # Apply custom shades
            alpha=0.7
        )
        plt.title("Puncta vs Intensity: VGAT vs VGLUT2_Thresholding Highlighted", fontsize=14)
        plt.xlabel("Intensity")
        plt.ylabel("Puncta Count")
        plt.legend(title="Subpopulation", loc="upper right")
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, "Subpopulation_Scatter.png"))
        plt.close()

    else:
        print("No data available for visualization.")

    # Ensure there is data left after filtering for the joint plot
    if not filtered_df.empty:
        # **PLOT2: Joint plot (filtered Puncta > 2, Intensity > 120)**
        joint_plot = sns.jointplot(
            data=filtered_df,
            x="Intensity",
            y="Puncta",
            hue="Cell Type",  # Correctly mapped names
            palette="Set2"
        )
        joint_plot.savefig(os.path.join(plots_dir, "Filtered_VGAT_vs_VGLUT2_JointPlot.png"))
        plt.close()
    else:
        print("No data points meet the cutoff (Puncta > 2 and Intensity > 120). Skipping joint plot.")