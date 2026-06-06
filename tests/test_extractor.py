import os
import sys

import pathlib
ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())
sys.path.append(ROOT_DIR)

from src.core.extractor import extract_video_sequence
print("=" * 60)
print("IntentFlow - Single-Video Isolated Sandbox Test")
print("=" * 60)

RAW_DATA_DIR = os.path.expanduser("~/IntentFlow/data/raw")
test_class = "PushUps"
class_folder = os.path.join(RAW_DATA_DIR, test_class)

# Check if we have our downloaded sample video ready
if not os.path.exists(class_folder) or len(os.listdir(class_folder)) == 0:
    print(f"⚠️ Test aborted: File missing. Make sure data/raw/{test_class}/sample_0.mp4 exists.")
else:
    # Find the sample_0.mp4 video we just downloaded
    test_file = [f for f in os.listdir(class_folder) if f.endswith(('.avi', '.mp4'))][0]
    target_path = os.path.join(class_folder, test_file)
    
    print(f"Processing sample target: {target_path}")
    
    # Run our extraction assembly line!
    sequence = extract_video_sequence(target_path)
    
    print(f"\nExtracted sequence matrix shape: {sequence.shape}")
    print(f"Expected AI model input shape   : (30, 132)")
    
    if sequence.shape == (30, 132):
        print("\nSTATUS: Sandbox test PASSED! MediaPipe is extracting skeleton numbers perfectly.")
    else:
        print("\nSTATUS: Sandbox test FAILED. Size mismatch.")
print("=" * 60)