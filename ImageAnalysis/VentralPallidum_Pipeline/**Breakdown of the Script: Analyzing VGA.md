# README: Intensity and Puncta Analysis Script

## Overview
This script processes and analyzes whole-slide image data for **VGAT and VGLUT2 OPRM1** composite detections. It incorporates **outlier exclusion and intensity thresholding** from the intensity analysis script and applies it to both intensity and puncta data.

## Features
- Loads **raw detection data** for VGAT and VGLUT2.
- Applies **outlier removal** using the **Interquartile Range (IQR) method**.
- Dynamically determines an **intensity threshold** using peak-valley analysis.
- Performs statistical analysis (Mann-Whitney U test).
- Generates plots for visualization.

## Dependencies
Ensure you have the following Python libraries installed:
```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Usage
Run the script using:
```bash
python updated_intensityANDpuncta_vgatvglut2oprm1_plots.py
```

## Key Functions
### `remove_outliers(df, column)`
Removes outliers based on the IQR method:
```python
import numpy as np

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
```

### `calculate_threshold(df, column)`
Dynamically calculates an **intensity threshold**:
```python
from scipy.signal import find_peaks

def calculate_threshold(df, column):
    density = gaussian_kde(df[column])
    x = np.linspace(df[column].min(), df[column].max(), 1000)
    y = density(x)
    peaks, _ = find_peaks(y)
    valleys, _ = find_peaks(-y)
    threshold = x[valleys[0]] if len(valleys) > 0 else df[column].median()
    return threshold
```

## Output
- **Plots** saved in the `oprm1VGATvsVGLUT2_plots/` directory.
- **Statistical results** printed to the console.

## Notes
- Ensure the raw detection files are located in the correct paths before running the script.
- Modify the `paths` dictionary if file locations change.


