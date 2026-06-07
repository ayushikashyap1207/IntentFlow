from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import numpy as np

from ..database import supabase
from ..models.session import SessionResponse
from .groq_service import generate_clinical_report
from .inference import run_inference


def _reshape_sequence(sequence: np.ndarray) -> np.ndarray:
    array = np.asarray(sequence, dtype=np.float32)
    if array.ndim == 3:
        array = array.reshape(-1, array.shape[-1])
    elif array.ndim == 1:
        array = array.reshape(1, -1)
    return array


def _joint(frame: np.ndarray, index: int) -> np.ndarray:
    start = index * 4
    return frame[start : start + 3]


def _calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
    v1 = p1 - p2
    v2 = p3 - p2
    magnitude1 = np.linalg.norm(v1)
    magnitude2 = np.linalg.norm(v2)
    if magnitude1 == 0 or magnitude2 == 0:
        return 180.0
    cosine = np.dot(v1, v2) / (magnitude1 * magnitude2)
    return float(np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0))))


def _extract_joint_angles(sequence: np.ndarray) -> dict[str, list[float]]:
    reshaped = _reshape_sequence(sequence)
    knee_angles: list[float] = []
    hip_angles: list[float] = []
    ankle_angles: list[float] = []

    for frame in reshaped:
        if frame.size < 132:
            frame = np.pad(frame, (0, 132 - frame.size))

        left_shoulder = _joint(frame, 11)
        left_hip = _joint(frame, 23)
        left_knee = _joint(frame, 25)
        left_ankle = _joint(frame, 27)
        left_heel = _joint(frame, 29)

        knee_angles.append(_calculate_angle(left_hip, left_knee, left_ankle))
        hip_angles.append(_calculate_angle(left_shoulder, left_hip, left_knee))
        ankle_angles.append(_calculate_angle(left_knee, left_ankle, left_heel))

    return {'knee': knee_angles, 'hip': hip_angles, 'ankle': ankle_angles}


def _estimate_reps(knee_angles: list[float], minimum: int = 10, maximum: int = 15) -> int:
    frame_count = len(knee_angles)
    if frame_count <= 1:
        return minimum
    estimated = max(minimum, min(maximum, frame_count // 2))
    return max(minimum, estimated)


def _sample_series(series: list[float], count: int) -> list[float]:
    if not series:
        return [0.0] * count

    indices = np.linspace(0, len(series) - 1, num=count)
    sampled = [float(series[int(round(index))]) for index in indices]
    if len(sampled) < count:
        sampled.extend([sampled[-1]] * (count - len(sampled)))
    return sampled[:count]


def _build_chart_data(knee: list[float], hip: list[float], ankle: list[float], rep_count: int) -> list[dict[str, float]]:
    knee_sample = _sample_series(knee, rep_count)
    hip_sample = _sample_series(hip, rep_count)
    ankle_sample = _sample_series(ankle, rep_count)

    return [
        {
            'rep': index + 1,
            'knee': round(knee_sample[index], 2),
            'hip': round(hip_sample[index], 2),
            'ankle': round(ankle_sample[index], 2),
        }
        for index in range(rep_count)
    ]


def _fetch_patient(patient_id: str) -> dict[str, Any]:
    response = supabase.table('patients').select('*').eq('id', patient_id).limit(1).execute()
    if not response.data:
        raise ValueError(f'Patient not found: {patient_id}')
    return response.data[0]


def _save_session(session_payload: dict[str, Any]) -> dict[str, Any]:
    response = supabase.table('sessions').insert(session_payload).execute()
    if not response.data:
        return session_payload
    return response.data[0]


def build_full_report(patient_id: str, exercise: str, sequence: np.ndarray) -> SessionResponse:
    patient = _fetch_patient(patient_id)
    sequence_array = _reshape_sequence(sequence)
    joint_angles = _extract_joint_angles(sequence_array)
    rep_count = _estimate_reps(joint_angles['knee'])

    inference_result = run_inference(sequence_array)
    sequence_stats = {
        'avg_angles': {
            'knee': float(np.mean(joint_angles['knee'])) if joint_angles['knee'] else 0.0,
            'hip': float(np.mean(joint_angles['hip'])) if joint_angles['hip'] else 0.0,
            'ankle': float(np.mean(joint_angles['ankle'])) if joint_angles['ankle'] else 0.0,
        },
        'variance': {
            'knee': float(np.var(joint_angles['knee'])) if joint_angles['knee'] else 0.0,
            'hip': float(np.var(joint_angles['hip'])) if joint_angles['hip'] else 0.0,
            'ankle': float(np.var(joint_angles['ankle'])) if joint_angles['ankle'] else 0.0,
        },
        'rep_count': rep_count,
    }

    clinical_report = generate_clinical_report(
        exercise=exercise,
        predicted_class=inference_result['predicted_class'],
        confidence=inference_result['confidence'],
        sequence_stats=sequence_stats,
    )

    chart_data = _build_chart_data(joint_angles['knee'], joint_angles['hip'], joint_angles['ankle'], rep_count)
    session_id = str(uuid4())
    session_date = datetime.now(timezone.utc).isoformat()

    session_payload = {
        'id': session_id,
        'patient_id': patient_id,
        'patient_name': patient.get('name', 'Unknown Patient'),
        'exercise': exercise,
        'date': session_date,
        'risk_level': clinical_report['risk_level'],
        'form_score': float(clinical_report['form_score']),
        'reps_analysed': rep_count,
        'avg_knee_angle': float(sequence_stats['avg_angles']['knee']),
        'confidence': float(inference_result['confidence']),
        'diagnosis': clinical_report['diagnosis'],
        'prescription': clinical_report['prescription'],
        'kinematics': clinical_report['kinematics'],
        'detected_issues': clinical_report['detected_issues'],
        'references': clinical_report['references'],
        'chart_data': chart_data,
        'predicted_class': inference_result['predicted_class'],
        'class_probabilities': inference_result['class_probabilities'],
        'raw_predictions': inference_result['raw_predictions'],
        'sequence_stats': sequence_stats,
    }

    saved_session = _save_session(session_payload)

    return SessionResponse(
        id=str(saved_session.get('id', session_id)),
        patient_id=str(saved_session.get('patient_id', patient_id)),
        patient_name=str(saved_session.get('patient_name', patient.get('name', 'Unknown Patient'))),
        exercise=str(saved_session.get('exercise', exercise)),
        date=str(saved_session.get('date', session_date)),
        risk_level=saved_session.get('risk_level', clinical_report['risk_level']),
        form_score=float(saved_session.get('form_score', clinical_report['form_score'])),
        reps_analysed=int(saved_session.get('reps_analysed', rep_count)),
        avg_knee_angle=float(saved_session.get('avg_knee_angle', sequence_stats['avg_angles']['knee'])),
        confidence=float(saved_session.get('confidence', inference_result['confidence'])),
        diagnosis=str(saved_session.get('diagnosis', clinical_report['diagnosis'])),
        prescription=str(saved_session.get('prescription', clinical_report['prescription'])),
        kinematics=str(saved_session.get('kinematics', clinical_report['kinematics'])),
        detected_issues=list(saved_session.get('detected_issues', clinical_report['detected_issues'])),
        references=list(saved_session.get('references', clinical_report['references'])),
        chart_data=list(saved_session.get('chart_data', chart_data)),
    )
