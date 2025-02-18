import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
import random
import seaborn as sns
import math

# Define dataset path
dataset_dir = "/Users/jamieannemortel/BrainTumorMRI_Dataset"
train_dir = os.path.join(dataset_dir, "train")

# Get class names (folder names), excluding hidden files like .DS_Store
class_names = [c for c in os.listdir(train_dir) if not c.startswith(".")]

# Number of columns for the grid
num_cols = 4  # Fixed number of columns

# Select a random number of images from different classes
max_images = 12  # Set an upper limit
num_images = min(max_images, sum(len(os.listdir(os.path.join(train_dir, c))) for c in class_names))  # Ensure valid count

selected_images = []
selected_labels = []

for _ in range(num_images):
    class_name = random.choice(class_names)  # Pick a random class
    class_path = os.path.join(train_dir, class_name)
    
    # Ensure the class has images before choosing
    image_files = [f for f in os.listdir(class_path) if not f.startswith(".")]
    if not image_files:
        continue
    
    image_name = random.choice(image_files)  # Pick a random image
    img_path = os.path.join(class_path, image_name)

    selected_images.append(img_path)
    selected_labels.append(class_name)

# Determine the number of rows dynamically
num_rows = math.ceil(num_images / num_cols)  

# Create the figure and axes dynamically
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
fig.subplots_adjust(hspace=0.5)

# Flatten axes array for easy iteration
axes = axes.flatten()  

# Plot images
for i in range(num_images):
    img = load_img(selected_images[i], target_size=(256, 256))  # Load image
    axes[i].imshow(img)  
    axes[i].set_title(selected_labels[i])  # Set class label as title
    axes[i].axis("off")  # Hide axis

# Hide any extra subplots if they exist
for i in range(num_images, len(axes)):  
    axes[i].axis("off")

plt.show()
