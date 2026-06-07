import os
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Configuration Dimensions
SEQUENCE_LENGTH = 30  # Fixed sequence window length expected by Phase 3 LSTM
FEATURE_SIZE = 132    # 33 landmarks * 4 values (x, y, z, presence)

import pathlib

# Locate the task asset safely at the project root dynamically
ROOT_DIR = str(pathlib.Path(__file__).parent.parent.parent.resolve())
TASK_PATH = os.path.join(ROOT_DIR, "pose_landmarker.task")

if not os.path.exists(TASK_PATH):
    raise FileNotFoundError(f"Critical Task Asset missing at: {TASK_PATH}. Please make sure pose_landmarker.task is in your root IntentFlow folder.")

# Configure the local Tasks Engine Options
base_options = python.BaseOptions(model_asset_path=TASK_PATH)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    output_segmentation_masks=False
)

def extract_keypoints(landmarker_result):
    """
    Extracts 33 pose landmarks with 4 dimensions each (x, y, z, presence).
    Flattens the data safely into a 1D vector of shape (132,).
    """
    if landmarker_result and landmarker_result.pose_landmarks:
        # Isolate the primary person tracked in the frame bounds
        first_person_landmarks = landmarker_result.pose_landmarks[0]
        pose = np.array([
            [lm.x, lm.y, lm.z, lm.presence]
            for lm in first_person_landmarks
        ]).flatten()
    else:
        # Fallback padding to protect dimensional stability if human frame fails to capture
        pose = np.zeros(FEATURE_SIZE)
    return pose

def extract_video_sequence(video_path, seq_length=SEQUENCE_LENGTH):
    """
    Reads a target video path frame-by-frame, runs high-speed inference,
    and returns a clean sequence array of shape (30, 132).
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    with vision.PoseLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened() and len(frames) < seq_length:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Normalize frame color mappings for MediaPipe Tasks pipeline
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
            
            # Execute physical keypoint extraction
            detection_result = landmarker.detect(mp_image)
            keypoints = extract_keypoints(detection_result)
            frames.append(keypoints)
            
    cap.release()
    
    # Pad shorter sequence arrays with structural zeros if clip duration under-runs target length
    while len(frames) < seq_length:
        frames.append(np.zeros(FEATURE_SIZE))
        
    return np.array(frames[:seq_length])

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)

    # Loop through the detected poses to visualize.
    for idx in range(len(pose_landmarks_list)):
        pose_landmarks = pose_landmarks_list[idx]

        # Draw the pose landmarks.
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
    return annotated_image

def process_live_frame(frame, landmarker):
    """
    Processes a single live frame, returning the annotated frame and the extracted feature vector.
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    
    # Execute extraction
    detection_result = landmarker.detect(mp_image)
    
    # Draw skeleton
    annotated_frame = draw_landmarks_on_image(frame, detection_result)
    
    # Extract features
    features = extract_keypoints(detection_result)
    
    return annotated_frame, features