from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

try:
    import tensorflow as tf
except Exception:  # pragma: no cover - import-time fallback for partial environments
    tf = None  # type: ignore[assignment]

from ..config import PROJECT_ROOT, settings

EXERCISE_CLASSES = [
    'PushUps',
    'TaiChi',
    'Squats_Rehab',
    'Shoulder_Abduction',
    'Knee_Extension',
    'Hip_Abduction',
    'Lunges',
    'Ankle_Dorsiflexion',
]


@lru_cache(maxsize=1)
def _load_interpreter() -> tf.lite.Interpreter:
    if tf is None:
        raise RuntimeError('TensorFlow is not installed')

    model_path = Path(settings.tflite_model_path)
    if not model_path.is_absolute():
        model_path = (PROJECT_ROOT / model_path).resolve()

    if not model_path.exists():
        raise FileNotFoundError(f'Model file not found: {model_path}')

    interpreter = tf.lite.Interpreter(model_path=str(model_path))
    interpreter.allocate_tensors()
    return interpreter


def is_model_loaded() -> bool:
    if tf is None:
        return False

    try:
        _load_interpreter()
        return True
    except Exception as exc:
        print(f'Model health check failed: {exc}')
        return False


def _prepare_sequence(sequence: np.ndarray) -> np.ndarray:
    array = np.asarray(sequence, dtype=np.float32)
    if array.ndim == 2:
        array = np.expand_dims(array, axis=0)
    elif array.ndim == 1:
        array = np.expand_dims(np.expand_dims(array, axis=0), axis=0)
    return array


def _fit_to_input_shape(sequence: np.ndarray, input_shape: np.ndarray) -> np.ndarray:
    array = np.asarray(sequence, dtype=np.float32)
    if array.ndim != 3:
        array = _prepare_sequence(array)

    target_timesteps = int(input_shape[1]) if len(input_shape) > 1 and input_shape[1] > 0 else array.shape[1]
    target_features = int(input_shape[2]) if len(input_shape) > 2 and input_shape[2] > 0 else array.shape[2]

    if array.shape[1] < target_timesteps:
        padding = np.zeros((array.shape[0], target_timesteps - array.shape[1], array.shape[2]), dtype=np.float32)
        array = np.concatenate([array, padding], axis=1)
    elif array.shape[1] > target_timesteps:
        array = array[:, :target_timesteps, :]

    if array.shape[2] < target_features:
        padding = np.zeros((array.shape[0], array.shape[1], target_features - array.shape[2]), dtype=np.float32)
        array = np.concatenate([array, padding], axis=2)
    elif array.shape[2] > target_features:
        array = array[:, :, :target_features]

    return array.astype(np.float32)


def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - np.max(values)
    exp_values = np.exp(shifted)
    total = np.sum(exp_values)
    if total == 0:
        return np.ones_like(values) / len(values)
    return exp_values / total


def run_inference(sequence: np.ndarray) -> dict[str, Any]:
    if tf is None:
        raise RuntimeError('Model not loaded')

    interpreter = _load_interpreter()
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    sample_sequence = _fit_to_input_shape(_prepare_sequence(sequence), input_details['shape'])

    interpreter.set_tensor(input_details['index'], sample_sequence)
    interpreter.invoke()

    raw_output = interpreter.get_tensor(output_details['index'])[0]
    probabilities = _softmax(raw_output.astype(np.float32))
    top_index = int(np.argmax(probabilities))

    class_probabilities = {
        exercise: float(probabilities[index]) for index, exercise in enumerate(EXERCISE_CLASSES[: len(probabilities)])
    }

    return {
        'predicted_class': EXERCISE_CLASSES[top_index],
        'confidence': float(probabilities[top_index]),
        'class_probabilities': class_probabilities,
        'raw_predictions': [float(value) for value in raw_output.tolist()],
    }
