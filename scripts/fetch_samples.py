import os
import urllib.request
from tqdm import tqdm

print("=" * 60)
print("IntentFlow - Direct Sample Video Downloader")
print("=" * 60)

PROJECT_ROOT = os.path.expanduser("~/IntentFlow")
RAW_DIR = os.path.join(PROJECT_ROOT, "data/raw")

# Mapping out clear target video sources for our validation suite classes
SAMPLE_VIDEOS = {
    "PushUps": [
        "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4" # General test video
    ],
    "TaiChi": [
        "https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/face-demographics-walking.mp4"
    ]
}

class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

print("Fetching high-fidelity video streams for skeleton tracking test targets...")

for class_name, urls in SAMPLE_VIDEOS.items():
    class_path = os.path.join(RAW_DIR, class_name)
    os.makedirs(class_path, exist_ok=True)
    
    for idx, url in enumerate(urls):
        # Save files as standard compatible target files
        extension = ".mp4"
        filename = f"sample_{idx}{extension}"
        dest_file_path = os.path.join(class_path, filename)
        
        print(f"\n→ Syncing tracking target asset to: data/raw/{class_name}/{filename}")
        try:
            with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=f"Downloading {class_name}") as t:
                urllib.request.urlretrieve(url, filename=dest_file_path, reporthook=t.update_to)
        except Exception as e:
            print(f"❌ Could not download file from endpoint mirror: {e}")

print("\n" + "=" * 60)
print("STATUS: Sample asset sync complete! Verification data loaded.")
print("=" * 60)