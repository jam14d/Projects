import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator  
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications import VGG16  

# Define dataset paths
DATASET_DIR = "/Users/jamieannemortel/BrainTumorMRI_Dataset" 

def check_directories():
    """Check if dataset directories exist."""
    train_dir = os.path.join(DATASET_DIR, "train")
    val_dir = os.path.join(DATASET_DIR, "val")
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        raise FileNotFoundError("Training or validation directory not found!")
    
    return train_dir, val_dir

def build_model():
    """Build and compile the CNN model using transfer learning."""
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze some layers
    for layer in base_model.layers[:-5]:  # Unfreeze last 5 layers
        layer.trainable = True

    model = Sequential([
        base_model,  
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(4, activation='softmax')  
    ])

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    
    return model

def get_data_generators(train_dir, val_dir):
    """Create data generators for training and validation."""
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir, target_size=(224, 224), batch_size=32, class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir, target_size=(224, 224), batch_size=32, class_mode='categorical'
    )

    return train_generator, val_generator

def train_and_save_model(model, train_generator, val_generator, epochs=10):
    """Train the model and save it after training."""
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        verbose=1
    )
    model.save("brain_tumor_model.h5")
    print("Model saved as 'brain_tumor_model.h5'")
    return history

# Run the full training process
train_dir, val_dir = check_directories()
model = build_model()
train_generator, val_generator = get_data_generators(train_dir, val_dir)
history = train_and_save_model(model, train_generator, val_generator)

