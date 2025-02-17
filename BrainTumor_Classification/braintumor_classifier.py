import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator  
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.applications import VGG16  
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns

# Set the path to your dataset (UPDATE THIS to your actual dataset directory)
dataset_dir = "/Users/jamieannemortel/BrainTumorMRI_Dataset" 
train_dir = os.path.join(dataset_dir, "train")
val_dir = os.path.join(dataset_dir, "val")
test_dir = os.path.join(dataset_dir, "test")

# Check if paths exist
print("Training Directory Exists:", os.path.exists(train_dir))
print("Validation Directory Exists:", os.path.exists(val_dir))
print("Test Directory Exists:", os.path.exists(test_dir))

# Load pre-trained VGG16 without the top classifier layers (feature extractor)
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model's layers so they are not updated during training
for layer in base_model.layers:
    layer.trainable = False

# Build the full model (adding custom classification layers on top of VGG16)
model = Sequential([
    base_model,  # Use the pre-trained model as a feature extractor
    Flatten(),  # Flatten the extracted features
    Dense(256, activation='relu'),  # Fully connected layer with ReLU activation
    Dropout(0.5),  # Dropout to reduce overfitting
    Dense(4, activation='softmax')  # Output layer with 4 classes (softmax for multi-class classification)
])

# Compile the model for multi-class classification
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss='categorical_crossentropy',  # Multi-class classification loss
              metrics=['accuracy'])  # Tracking accuracy during training

# Print the model summary to understand its structure
model.summary()

# Prepare image data generators (to load images & apply data augmentation)
train_datagen = ImageDataGenerator(rescale=1./255)
val_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)  # No augmentation for test set

# Load training images
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'  # Multi-class classification
)

# Load validation images
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

# Load test images (to evaluate the model)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False  # Do not shuffle to match true labels correctly
)

# Train the model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10,  # Keep epochs low for testing purposes; increase for better accuracy
    verbose=1
)

# Evaluate model on test set
print("Evaluating Model on Test Data...")
y_true = test_generator.classes  # Get actual class labels

# Get model predictions (returns probabilities)
y_pred_probs = model.predict(test_generator)

# Convert probabilities to class labels
y_pred = np.argmax(y_pred_probs, axis=1)

# Compute evaluation metrics
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred, average='weighted')
recall = recall_score(y_true, y_pred, average='weighted')
f1 = f1_score(y_true, y_pred, average='weighted')

# Print evaluation results
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")

# Plot Confusion Matrix to visualize classification performance
conf_matrix = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6, 6))
sns.heatmap(conf_matrix, annot=True, cmap="Blues", fmt="d", 
            xticklabels=test_generator.class_indices.keys(), 
            yticklabels=test_generator.class_indices.keys())
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()