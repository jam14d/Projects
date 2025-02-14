import tensorflow as tf
import numpy as np

# Create random training data
X_train = np.random.rand(1000, 10)  # 1000 samples, 10 features
y_train = np.random.randint(2, size=(1000, 1))  # Binary labels (0 or 1)

# Build a simple model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model for a few epochs
model.fit(X_train, y_train, epochs=5, batch_size=32)

# Print success message
print("✅ TensorFlow test passed!")
