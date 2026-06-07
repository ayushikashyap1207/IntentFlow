from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..database import health_check_supabase
from ..models.session import AnalysisRequest, AnalysisResponse
from ..services.groq_service import is_groq_available
from ..services.inference import is_model_loaded
from ..services.mediapipe_service import extract_landmarks_from_video, is_mediapipe_available
from ..services.report_service import build_full_report

router = APIRouter()


class SequencePayload(AnalysisRequest):
    sequence: list[list[float]]


@router.post('/analysis/video', response_model=AnalysisResponse)
async def analyze_video(
    patient_id: str = Form(...),
    exercise: str = Form(...),
    file: UploadFile = File(...),
) -> AnalysisResponse:
    temp_path: str | None = None
    try:
        suffix = Path(file.filename or 'upload.mp4').suffix or '.mp4'
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = temp_file.name
            while chunk := await file.read(1024 * 1024):
                temp_file.write(chunk)

        sequence = extract_landmarks_from_video(temp_path)
        session = build_full_report(patient_id=patient_id, exercise=exercise, sequence=sequence)
        return AnalysisResponse(session=session, message='Video analysis completed successfully')
    except HTTPException:
        raise
    except Exception as exc:
        print(f'Error during video analysis: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to analyze video: {exc}') from exc
    finally:
        if temp_path:
            try:
                Path(temp_path).unlink(missing_ok=True)
            except Exception as cleanup_exc:
                print(f'Failed to remove temporary upload {temp_path}: {cleanup_exc}')


@router.post('/analysis/sequence', response_model=AnalysisResponse)
def analyze_sequence(payload: SequencePayload) -> AnalysisResponse:
    try:
        sequence = np.asarray(payload.sequence, dtype=np.float32)
        session = build_full_report(patient_id=payload.patient_id, exercise=payload.exercise, sequence=sequence)
        return AnalysisResponse(session=session, message='Sequence analysis completed successfully')
    except HTTPException:
        raise
    except Exception as exc:
        print(f'Error during sequence analysis: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to analyze sequence: {exc}') from exc


@router.get('/analysis/health')
def analysis_health() -> dict[str, object]:
    return {
        'model': is_model_loaded(),
        'mediapipe': is_mediapipe_available(),
        'groq': is_groq_available(),
        'supabase': health_check_supabase(),
    }
