from __future__ import annotations

from functools import lru_cache

import cv2
import numpy as np

try:
    import mediapipe as mp
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
except Exception:  # pragma: no cover - import-time fallback for partial environments
    mp = None  # type: ignore[assignment]
    python = None  # type: ignore[assignment]
    vision = None  # type: ignore[assignment]

from ..config import PROJECT_ROOT

FEATURE_SIZE = 132


@lru_cache(maxsize=1)
def _create_landmarker() -> vision.PoseLandmarker:
    if mp is None or python is None or vision is None:
        raise RuntimeError('MediaPipe is not installed')

    task_path = PROJECT_ROOT / 'pose_landmarker.task'
    if not task_path.exists():
        raise FileNotFoundError(f'Pose task file not found: {task_path}')

    base_options = python.BaseOptions(model_asset_path=str(task_path))
    options = vision.PoseLandmarkerOptions(
        base_options=base_options,
        output_segmentation_masks=False,
        running_mode=vision.RunningMode.IMAGE,
    )
    return vision.PoseLandmarker.create_from_options(options)


def is_mediapipe_available() -> bool:
    if mp is None or python is None or vision is None:
        return False

    try:
        _create_landmarker()
        return True
    except Exception as exc:
        print(f'MediaPipe health check failed: {exc}')
        return False


def _extract_pose_vector(landmarker_result: vision.PoseLandmarkerResult | None) -> np.ndarray:
    if landmarker_result and landmarker_result.pose_landmarks:
        landmarks = landmarker_result.pose_landmarks[0]
        pose = np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in landmarks], dtype=np.float32)
        return pose.flatten()
    return np.zeros(FEATURE_SIZE, dtype=np.float32)


def extract_landmarks_from_frame(frame: np.ndarray) -> np.ndarray:
    if mp is None:
        raise RuntimeError('MediaPipe is not installed')

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    landmarker = _create_landmarker()
    result = landmarker.detect(mp_image)
    return _extract_pose_vector(result)


def extract_landmarks_from_video(video_path: str) -> np.ndarray:
    if mp is None:
        raise RuntimeError('MediaPipe is not installed')

    cap = cv2.VideoCapture(video_path)
    frames: list[np.ndarray] = []
    landmarker = _create_landmarker()

    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = landmarker.detect(mp_image)
            frames.append(_extract_pose_vector(result))
    finally:
        cap.release()

    if not frames:
        return np.zeros((1, FEATURE_SIZE), dtype=np.float32)

    sequence = np.vstack(frames).astype(np.float32)
    if sequence.shape[1] != FEATURE_SIZE:
        sequence = sequence[:, :FEATURE_SIZE]
        if sequence.shape[1] < FEATURE_SIZE:
            padding = np.zeros((sequence.shape[0], FEATURE_SIZE - sequence.shape[1]), dtype=np.float32)
            sequence = np.concatenate([sequence, padding], axis=1)
    return sequence
