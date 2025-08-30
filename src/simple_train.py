import tensorflow as tf 
from tensorflow import keras 
from keras.models import Sequential 
from keras.layers import Dense, Flatten 
import numpy as np 

# --- 1. Prepare Your Data --- 
# This is a placeholder for your actual data loading and preprocessing 
# Assume you have: 
# X_train: your training data (e.g., a NumPy array of shape [number_of_samples, window_size, 6]) 
# y_train: your one-hot encoded training labels (e.g., a NumPy array of shape [number_of_samples, 4]) 

# Example placeholder data 
X_train = np.random.rand(100, 50, 6) # 100 samples, window size of 50, 6 features 
y_train = tf.keras.utils.to_categorical(np.random.randint(4, size=(100, 1)), num_classes=4) # 100 labels for 4 classes 

# --- 2. Define Your Model --- 
model_name = "my_gesture_model" 
activation_function = "relu" 

model = Sequential(name=model_name) 

# The Flatten layer converts the 2D window of data into a 1D array 
model.add(Flatten(input_shape=(50, 6))) # Adjust input_shape to your window size and number of features 

# Add your hidden layers with the specified activation function 
model.add(Dense(128, activation=activation_function)) 
model.add(Dense(64, activation=activation_function)) 

# Add the final output layer with 4 neurons (for your 3 gestures + "other") and a softmax activation 
model.add(Dense(4, activation="softmax")) 

# --- 3. Compile the Model --- 
model.compile(optimizer='adam', 
             loss='categorical_crossentropy', 
             metrics=['accuracy']) 

# Print a summary of your model's architecture 
model.summary() 

# --- 4. Train the Model --- 
model.fit(X_train, y_train, epochs=10, batch_size=32) 

# --- 5. Save the Trained Model --- 
model.save(f"{model_name}.h5") 

print(f"Model trained and saved as {model_name}.h5") 