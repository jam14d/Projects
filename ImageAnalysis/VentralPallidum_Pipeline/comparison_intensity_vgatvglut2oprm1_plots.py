import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu, ks_2samp
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde
import numpy as np
from statannotations.Annotator import Annotator

# Define paths for VGAT and VGLUT2 data
paths = {
    "vgat": {
        "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGAT_OPRM1_COMPOSITE/detections_iteration4_vgatwithMu_12.13.24",
    },
    "vglut2": {
        "raw_detection": r"/Volumes/backup driv/VP_qp_LF - ITERATION4 - VGLUT2_OPRM1_COMPOSITE/detections_iteration4_vglut2withMu_12.13.24",
    },
}

# Function to convert Windows paths to Unix-like paths if running in a Unix environment
def convert_to_unix_path(win_path):
    if os.name != "nt":
        win_path = win_path.replace("\\", "/")
        if win_path[1:3] == ":/":
            return f"/mnt/{win_path[0].lower()}{win_path[2:]}"
    return win_path

# Convert all paths to Unix-like if necessary
for group in paths:
    paths[group] = {key: convert_to_unix_path(value) for key, value in paths[group].items()}

# Create a "plots" directory in the same location as the script
script_dir = os.path.dirname(os.path.abspath(__file__))
plots_dir = os.path.join(script_dir, "oprm1VGATvsVGLUT2_plots_intensity")
os.makedirs(plots_dir, exist_ok=True)

# Define classifications and colors
classifications = {
    "vgat_positive_oprm1_positive": ["vgat_Pos: oprm1_Pos"],
    "vglut2_positive_oprm1_positive": ["vglut2_Pos: oprm1_Pos"],
}
colors = {
    "vgat_positive_oprm1_positive": "#81daca",
    "vglut2_positive_oprm1_positive": "#ff8559",  # Shade of orange
}

# Initialize a dictionary to collect data for each classification
data = {key: [] for key in classifications.keys()}


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


# Function to calculate the threshold (valley between peaks) dynamically
def calculate_threshold(df, column):
    if df.empty:
        return None
    
    # Fit KDE
    kde = gaussian_kde(df[column])
    x = np.linspace(df[column].min(), df[column].max(), 1000)
    y = kde(x)
    
    # Find peaks and valleys
    peaks, _ = find_peaks(y)
    valleys, _ = find_peaks(-y)

    if len(valleys) > 0:
        # Select the first valley as the threshold (or customize based on domain knowledge)
        threshold = x[valleys[0]]
        return threshold
    else:
        return None  # Return None if no valleys are found


# Updated helper function to process files and extract relevant data
def collect_data(paths, classification_key, labels):
    for file in os.listdir(paths["raw_detection"]):
        if file.endswith(".txt"):
            try:
                det_data = pd.read_csv(os.path.join(paths["raw_detection"], file), sep="\t", encoding="utf-8")
                if "Classification" not in det_data.columns:
                    print(f"Skipping file {file}: 'Classification' column is missing.")
                    continue
                # Filter by classification
                cell_data = det_data[det_data["Classification"].isin(labels)]
                
                # Append filtered data
                data[classification_key].append(cell_data[[
                    "AF568: Cell: Mean", 
                    "Subcellular: Channel 2: Num spots estimated"
                ]].dropna())
            except UnicodeDecodeError:
                print(f"Encoding error in file {file}: Skipping.")
            except Exception as e:
                print(f"Error processing {file}: {e}")

# Collect original data (no thresholding)
original_data = {key: [] for key in classifications.keys()}
for group, labels in classifications.items():
    if "vgat" in group:
        collect_data(paths["vgat"], group, labels)
    elif "vglut2" in group:
        collect_data(paths["vglut2"], group, labels)
    if data[group]:
        original_data[group] = pd.concat(data[group], ignore_index=True)
    else:
        original_data[group] = pd.DataFrame(columns=["AF568: Cell: Mean", "Subcellular: Channel 2: Num spots estimated"])

# Calculate thresholds for VGAT and VGLUT2
thresholds = {}
for key, df in original_data.items():
    thresholds[key] = calculate_threshold(df, "AF568: Cell: Mean")
    print(f"Threshold for {key}: {thresholds[key]}")


# Apply dynamic thresholds to trim data
trimmed_data = {}
for key, df in original_data.items():
    if thresholds[key] is not None:
        filtered_df = df[df["AF568: Cell: Mean"] > thresholds[key]]  # Apply calculated threshold
        trimmed_data[key] = remove_outliers(filtered_df, "AF568: Cell: Mean")
    else:
        trimmed_data[key] = pd.DataFrame()  # Empty DataFrame if no threshold found


# # Function to compare plots before and after trimming
# def compare_plots(original_df, trimmed_df, column, title, color):
#     plt.figure(figsize=(16, 8))
    
#     # Original data distribution (starting from 0)
#     plt.subplot(2, 2, 1)
#     sns.histplot(original_df[column], kde=True, bins=30, color=color, alpha=0.7)
#     plt.title(f"{title} (Original Data Distribution)")
#     plt.xlabel("OPRM1 Intensity")  # Updated label
#     plt.xlim(0, None)  # Start x-axis from 0
    
#     plt.subplot(2, 2, 2)
#     sns.boxplot(x=original_df[column], color=color)
#     plt.title(f"{title} (Original Box Plot)")
#     plt.xlabel("OPRM1 Intensity")  # Updated label
#     plt.xlim(0, None)  # Start x-axis from 0

#     # Trimmed data distribution (starting from 0)
#     plt.subplot(2, 2, 3)
#     sns.histplot(trimmed_df[column], kde=True, bins=30, color=color, alpha=0.7)
#     plt.title(f"{title} (Trimmed Data Distribution)")
#     plt.xlabel("OPRM1 Intensity")  # Updated label
#     plt.xlim(115, None)  

#     plt.subplot(2, 2, 4)
#     sns.boxplot(x=trimmed_df[column], color=color)
#     plt.title(f"{title} (Trimmed Box Plot)")
#     plt.xlabel("OPRM1 Intensity")  # Updated label
#     plt.xlim(115, None)  

#     plt.tight_layout()
#     plt.savefig(os.path.join(plots_dir, f"{title.replace(' ', '_')}_comparison.png"))
#     plt.close()

# Function to compare plots before and after trimming, with peaks and thresholds
def compare_plots_with_peaks_and_threshold(original_df, trimmed_df, column, title, color, threshold):
    plt.figure(figsize=(16, 8))
    
    # Original Data Distribution
    plt.subplot(2, 2, 1)
    sns.histplot(original_df[column], kde=True, bins=30, color=color, alpha=0.7, label="Histogram")
    plt.title(f"{title} (Original Data Distribution)")
    plt.xlabel("OPRM1 Intensity")
    plt.xlim(0, None)
    
    # Add KDE and annotate peaks/thresholds
    kde = gaussian_kde(original_df[column])
    x = np.linspace(original_df[column].min(), original_df[column].max(), 1000)
    y = kde(x)
    peaks, _ = find_peaks(y)
    valleys, _ = find_peaks(-y)

    # Plot KDE
    plt.plot(x, y, color="blue", label="KDE", alpha=0.8)
    
    # Annotate Peaks
    for peak in peaks:
        plt.axvline(x[peak], color="green", linestyle="--", label=f"Peak @ {x[peak]:.2f}")
        plt.text(x[peak], y[peak] + 0.005, f"Peak: {x[peak]:.2f}", color="green", fontsize=8)
    
    # Annotate Threshold
    if threshold is not None:
        plt.axvline(threshold, color="red", linestyle="--", label=f"Threshold @ {threshold:.2f}")
        plt.text(threshold, max(y) * 0.8, f"Threshold: {threshold:.2f}", color="red", fontsize=10)

    plt.legend()

    # Box Plot for Original Data
    plt.subplot(2, 2, 2)
    sns.boxplot(x=original_df[column], color=color)
    plt.title(f"{title} (Original Box Plot)")
    plt.xlabel("OPRM1 Intensity")
    plt.xlim(0, None)

    # Trimmed Data Distribution
    plt.subplot(2, 2, 3)
    sns.histplot(trimmed_df[column], kde=True, bins=30, color=color, alpha=0.7, label="Histogram")
    plt.title(f"{title} (Trimmed Data Distribution)")
    plt.xlabel("OPRM1 Intensity")
    plt.xlim(threshold - 5 if threshold else 0, None)

    # Box Plot for Trimmed Data
    plt.subplot(2, 2, 4)
    sns.boxplot(x=trimmed_df[column], color=color)
    plt.title(f"{title} (Trimmed Box Plot)")
    plt.xlabel("OPRM1 Intensity")
    plt.xlim(threshold - 5 if threshold else 0, None)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, f"{title.replace(' ', '_')}_peaks_thresholds.png"))
    plt.close()

# Generate comparison plots for VGAT and VGLUT2 with peaks and thresholds
compare_plots_with_peaks_and_threshold(original_data["vgat_positive_oprm1_positive"], 
                                       trimmed_data["vgat_positive_oprm1_positive"], 
                                       "AF568: Cell: Mean", 
                                       "VGAT+ OPRM1+", 
                                       colors["vgat_positive_oprm1_positive"], 
                                       thresholds["vgat_positive_oprm1_positive"])

compare_plots_with_peaks_and_threshold(original_data["vglut2_positive_oprm1_positive"], 
                                       trimmed_data["vglut2_positive_oprm1_positive"], 
                                       "AF568: Cell: Mean", 
                                       "VGLUT2+ OPRM1+", 
                                       colors["vglut2_positive_oprm1_positive"], 
                                       thresholds["vglut2_positive_oprm1_positive"])

# # Generate comparison plots for VGAT and VGLUT2
# compare_plots(original_data["vgat_positive_oprm1_positive"], trimmed_data["vgat_positive_oprm1_positive"], 
#               "AF568: Cell: Mean", "VGAT+ OPRM1+", colors["vgat_positive_oprm1_positive"])
# compare_plots(original_data["vglut2_positive_oprm1_positive"], trimmed_data["vglut2_positive_oprm1_positive"], 
#               "AF568: Cell: Mean", "VGLUT2+ OPRM1+", colors["vglut2_positive_oprm1_positive"])

# Perform statistical tests between VGAT+ and VGLUT2+ groups for both original and trimmed data
stat_results = {"original": {}, "trimmed": {}}

# Statistical tests for original data
if not original_data["vgat_positive_oprm1_positive"].empty and not original_data["vglut2_positive_oprm1_positive"].empty:
    vgat_original = original_data["vgat_positive_oprm1_positive"]["AF568: Cell: Mean"]
    vglut2_original = original_data["vglut2_positive_oprm1_positive"]["AF568: Cell: Mean"]

    # Mann-Whitney U Test (original)
    u_stat, u_p_value = mannwhitneyu(vgat_original, vglut2_original, alternative='two-sided')
    stat_results["original"]["Mann-Whitney"] = (u_stat, u_p_value)

    # Kolmogorov-Smirnov Test (original)
    ks_stat, ks_p_value = ks_2samp(vgat_original, vglut2_original)
    stat_results["original"]["Kolmogorov-Smirnov"] = (ks_stat, ks_p_value)

# Statistical tests for trimmed data
if not trimmed_data["vgat_positive_oprm1_positive"].empty and not trimmed_data["vglut2_positive_oprm1_positive"].empty:
    vgat_trimmed = trimmed_data["vgat_positive_oprm1_positive"]["AF568: Cell: Mean"]
    vglut2_trimmed = trimmed_data["vglut2_positive_oprm1_positive"]["AF568: Cell: Mean"]

    # Mann-Whitney U Test
    u_stat, u_p_value = mannwhitneyu(vgat_trimmed, vglut2_trimmed, alternative='two-sided')
    stat_results["trimmed"]["Mann-Whitney"] = (u_stat, u_p_value)

    # Kolmogorov-Smirnov Test
    ks_stat, ks_p_value = ks_2samp(vgat_trimmed, vglut2_trimmed)
    stat_results["trimmed"]["Kolmogorov-Smirnov"] = (ks_stat, ks_p_value)

# Save results to a text file
stats_results_path = os.path.join(plots_dir, "statistical_tests_results.txt")
with open(stats_results_path, "w") as f:
    f.write("Statistical Test Results (Original Data):\n")
    for test_name, (stat, p_val) in stat_results["original"].items():
        f.write(f"{test_name}: Statistic = {stat}, p-value = {p_val}\n")
    f.write("\nStatistical Test Results (Trimmed Data):\n")
    for test_name, (stat, p_val) in stat_results["trimmed"].items():
        f.write(f"{test_name}: Statistic = {stat}, p-value = {p_val}\n")

# Generate descriptive statistics for original and trimmed data
descriptive_stats_path = os.path.join(plots_dir, "descriptive_statistics.txt")
with open(descriptive_stats_path, "w") as f:
    f.write("Descriptive Statistics for Original Data:\n")
    for key, df in original_data.items():
        f.write(f"\n{key}:\n")
        f.write(df.describe().to_string())
        f.write("\n")
    f.write("\nDescriptive Statistics for Trimmed Data:\n")
    for key, df in trimmed_data.items():
        f.write(f"\n{key}:\n")
        f.write(df.describe().to_string())
        f.write("\n")

print(f"Descriptive statistics saved to {descriptive_stats_path}")
print(f"Statistical test results saved to {stats_results_path}")
