import os
import shutil
import random

# Define paths (update these based on your structure)
train_dir = "/Users/jamieannemortel/BrainTumorMRI_Dataset/train"
val_dir = "/Users/jamieannemortel/BrainTumorMRI_Dataset/val"

# Set the validation split (e.g., 20% of training data)
val_split = 0.2

# Go through each class folder and move images
for class_name in ["glioma", "meningioma", "pituitary", "no_tumor"]:
    class_train_path = os.path.join(train_dir, class_name)
    class_val_path = os.path.join(val_dir, class_name)
    
    # Get list of all images in training class
    images = os.listdir(class_train_path)
    
    # Shuffle images randomly
    random.shuffle(images)
    
    # Calculate number of images to move
    num_val = int(len(images) * val_split)
    
    # Move images to validation folder
    for img in images[:num_val]:
        src_path = os.path.join(class_train_path, img)
        dst_path = os.path.join(class_val_path, img)
        shutil.move(src_path, dst_path)
    
    print(f"Moved {num_val} images from {class_name} to validation set.")

print("Validation set created successfully! 🚀")
