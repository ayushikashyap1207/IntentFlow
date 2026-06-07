import os
import numpy as np
import pathlib
import sys
import tensorflow as tf

# Force Python to track your project root directory cleanly
ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(ROOT_DIR)

from src.core.model import build_intentflow_model

# Input paths configuration
SEQ_DIR = os.path.join(ROOT_DIR, "data/sequences")
MODEL_EXPORT_DIR = os.path.join(ROOT_DIR, "models/saved")
os.makedirs(MODEL_EXPORT_DIR, exist_ok=True)

print("=" * 60)
print("IntentFlow - Neural Network Training Pipeline")
print("=" * 60)

# 1. Load data arrays generated from Phase 2
X = np.load(os.path.join(SEQ_DIR, "X_sequences.npy"))
y = np.load(os.path.join(SEQ_DIR, "y_labels.npy"))

print(f"Loaded feature matrix shape: {X.shape}")
print(f"Loaded label tracking shape: {y.shape}")

# Convert labels to categorical binary matrices
num_classes = len(np.unique(y))
y_categorical = tf.keras.utils.to_categorical(y, num_classes=num_classes)

# 2. Wiring Test fallback split logic
X_train, X_val, y_train, y_val = (X, X, y_categorical, y_categorical)

# 3. Instantiate the LSTM computational graph
model = build_intentflow_model(input_shape=(30, 132), num_classes=num_classes)

# Compile using Categorical Crossentropy loss and Adam optimizer
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

from tensorflow.keras.callbacks import EarlyStopping

print("\nBeginning Model Optimization Epochs...")
# Define early stopping to prevent overfitting on augmented data
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# 4. Fit network parameters over the loaded tracking points
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=50,  # Increased epochs for more robust training
    batch_size=4,
    callbacks=[early_stop],
    verbose=1
)

# 5. Export training artifacts locally
save_path = os.path.join(MODEL_EXPORT_DIR, "intentflow_lstm.keras")
model.save(save_path)

print("\n" + "-" * 60)
print("TRAINING STATUS SUMMARY")
print("-" * 60)
print(f"Final Training Accuracy   : {history.history['accuracy'][-1]:.4f}")
print(f"Model saved successfully to: models/saved/intentflow_lstm.keras")
print("=" * 60)
