import os
import pathlib
import sys
import tensorflow as tf
import numpy as np

# Force Python to track your project root directory cleanly
ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(ROOT_DIR)

KERAS_MODEL_PATH = os.path.join(ROOT_DIR, "models/saved/intentflow_lstm.keras")
TFLITE_OUTPUT_DIR = os.path.join(ROOT_DIR, "models/tflite")
os.makedirs(TFLITE_OUTPUT_DIR, exist_ok=True)
TFLITE_MODEL_PATH = os.path.join(TFLITE_OUTPUT_DIR, "intentflow_lstm.tflite")

print("=" * 60)
print("IntentFlow - TFLite Edge Optimization Engine (Stable Backend)")
print("=" * 60)

if not os.path.exists(KERAS_MODEL_PATH):
    raise FileNotFoundError(f"Source model file missing at: {KERAS_MODEL_PATH}")

print("Loading raw baseline .keras neural network...")
model = tf.keras.models.load_model(KERAS_MODEL_PATH)

print("Initializing Stable TFLite Functional Conversion...")
# We generate a concrete function from the model's signature to lock its types down
run_model = tf.function(lambda x: model(x))
concrete_func = run_model.get_concrete_function(
    tf.TensorSpec(shape=[1, 30, 132], dtype=tf.float32)
)

# Convert using the stable concrete function pathway instead of the abstract Keras graph
converter = tf.lite.TFLiteConverter.from_concrete_functions([concrete_func])

# Enforce stable target CPU sets
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS]

print("Compiling and optimizing mathematical graph weights...")
tflite_model = converter.convert()

print(f"Writing compressed artifact to storage layout...")
with open(TFLITE_MODEL_PATH, "wb") as f:
    f.write(tflite_model)

print("\n" + "-" * 60)
print("OPTIMIZATION STATUS SUMMARY")
print("-" * 60)
print(f"Optimized Model Present: {os.path.exists(TFLITE_MODEL_PATH)}")
print(f"TFLite Output Path     : models/tflite/intentflow_lstm.tflite")
print("=" * 60)
