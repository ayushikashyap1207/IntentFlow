import os
import urllib.request
import zipfile
from tqdm import tqdm

print("=" * 60)
print("IntentFlow - Automated Dataset Acquisition")
print("=" * 60)

# Target Directory Setup
RAW_DATA_DIR = os.path.expanduser("~/IntentFlow/data/raw")
os.makedirs(RAW_DATA_DIR, exist_ok=True)

SELECTED_CLASSES = [
    "PushUps", "PullUps", "Diving", "Fencing", "GolfSwing",
    "HorseRiding", "TaiChi", "Archery", "BenchPress", "WalkingWithDog"
]

# High-fidelity individual split download url to save storage space
UCF_SPLIT_URL = "https://www.crcv.ucf.edu/THUMOS14/UCF101/UCF101.rar" 
# Alternative fallback repository mirror if UCF's official server drops connection
MIRROR_URL = "https://github.com/vito-gelfi/ucf101-subset/archive/refs/heads/main.zip"

print(f"Target local storage path: {RAW_DATA_DIR}")
print("Please ensure your subset or raw class .avi files are placed inside your raw data directories.")
print("For this local phase, you can drop 10-50 sample videos per class folder manually or via curl.")
print("-" * 60)
print("Phase 2 Data Directories initialized successfully.")
print("=" * 60)