import os
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img
import random
import seaborn as sns

# Define dataset path
dataset_dir = "/Users/jamieannemortel/BrainTumorMRI_Dataset"
train_dir = os.path.join(dataset_dir, "train")

# Get class names (folder names), excluding hidden files like .DS_Store
class_names = [c for c in os.listdir(train_dir) if not c.startswith(".")]

# Number of images to display (3 rows × 4 columns = 12 images)
num_rows = 3
num_cols = 4
num_images = num_rows * num_cols

# Select random images from different classes
selected_images = []
selected_labels = []

for _ in range(num_images):
    class_name = random.choice(class_names)  # Pick a random class
    class_path = os.path.join(train_dir, class_name)
    image_name = random.choice(os.listdir(class_path))  # Pick a random image
    img_path = os.path.join(class_path, image_name)

    selected_images.append(img_path)
    selected_labels.append(class_name)

# Plot images in a grid
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 8))
fig.subplots_adjust(hspace=0.5)  # Space between images

for i, ax in enumerate(axes.flat):
    img = load_img(selected_images[i], target_size=(256, 256))  # Load image
    ax.imshow(img)  
    ax.set_title(selected_labels[i])  # Set class label as title
    ax.axis("off")  # Hide axis

plt.show()
