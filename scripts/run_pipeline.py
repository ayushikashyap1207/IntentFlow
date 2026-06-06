import os
import json
import numpy as np
import pathlib
import sys
from tqdm import tqdm

# Force Python to track your project directories cleanly
ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(ROOT_DIR)

from src.core.extractor import extract_video_sequence

RAW_DIR = os.path.join(ROOT_DIR, "data/raw")
SEQ_DIR = os.path.join(ROOT_DIR, "data/sequences")
os.makedirs(SEQ_DIR, exist_ok=True)

# The tracking behavior categories present in your raw workspace
SELECTED_CLASSES = ["PushUps", "TaiChi","Squat_rehab","shoulder_Abduction"]
LABEL_MAP = {cls: idx for idx, cls in enumerate(SELECTED_CLASSES)}

all_sequences = []
all_labels = []

print("=" * 60)
print("IntentFlow - Beginning Full Coordinate Processing Pipeline")
print("=" * 60)

for cls in SELECTED_CLASSES:
    cls_path = os.path.join(RAW_DIR, cls)
    if not os.path.exists(cls_path):
        print(f"Skipping {cls}: Directory missing.")
        continue
        
    # Read both modern mp4 and legacy avi formats seamlessly
    videos = [f for f in os.listdir(cls_path) if f.endswith(('.avi', '.mp4'))]
    print(f"\nProcessing behavioral sequence class: '{cls}' ({len(videos)} inputs found)")
    
    for video_file in tqdm(videos, desc=f"Extracting {cls}"):
        video_path = os.path.join(cls_path, video_file)
        try:
            sequence_matrix = extract_video_sequence(video_path)
            all_sequences.append(sequence_matrix)
            all_labels.append(LABEL_MAP[cls])
        except Exception as e:
            print(f"  Error processing video asset {video_file}: {e}")

# Compile numerical data arrays together
X = np.array(all_sequences)
y = np.array(all_labels)

print("\n" + "-" * 60)
print("PIPELINE COMPILATION SUMMARY")
print("-" * 60)
print(f"Final X matrix shape (Videos, Frames, Features): {X.shape}")
print(f"Final y tracking label array shape            : {y.shape}")
print(f"Any NaN/Null mathematical errors detected     : {np.isnan(X).any()}")

# Save array data files natively into your storage layer
np.save(os.path.join(SEQ_DIR, "X_sequences.npy"), X)
np.save(os.path.join(SEQ_DIR, "y_labels.npy"), y)

with open(os.path.join(SEQ_DIR, "label_map.json"), "w") as f:
    json.dump(LABEL_MAP, f, indent=2)

print("\nSTATUS: Success! Binary arrays generated safely inside data/sequences/.")
print("=" * 60)