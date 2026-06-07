from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ..database import supabase
from ..models.session import SessionResponse

router = APIRouter()


def _session_from_row(row: dict) -> SessionResponse:
    return SessionResponse(
        id=str(row['id']),
        patient_id=str(row['patient_id']),
        patient_name=str(row.get('patient_name', 'Unknown Patient')),
        exercise=str(row['exercise']),
        date=str(row['date']),
        risk_level=str(row.get('risk_level', 'LOW')).upper(),
        form_score=float(row.get('form_score', 0)),
        reps_analysed=int(row.get('reps_analysed', 0)),
        avg_knee_angle=float(row.get('avg_knee_angle', 0)),
        confidence=float(row.get('confidence', 0)),
        diagnosis=str(row.get('diagnosis', '')),
        prescription=str(row.get('prescription', '')),
        kinematics=str(row.get('kinematics', '')),
        detected_issues=list(row.get('detected_issues', [])),
        references=list(row.get('references', [])),
        chart_data=list(row.get('chart_data', [])),
    )


@router.get('/sessions', response_model=list[SessionResponse])
def list_sessions() -> list[SessionResponse]:
    try:
        response = supabase.table('sessions').select('*').order('date', desc=True).execute()
        return [_session_from_row(row) for row in response.data or []]
    except Exception as exc:
        print(f'Error listing sessions: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to list sessions: {exc}') from exc


@router.get('/sessions/{session_id}', response_model=SessionResponse)
def get_session(session_id: str) -> SessionResponse:
    try:
        response = supabase.table('sessions').select('*').eq('id', session_id).limit(1).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail='Session not found')
        return _session_from_row(response.data[0])
    except HTTPException:
        raise
    except Exception as exc:
        print(f'Error fetching session {session_id}: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to fetch session: {exc}') from exc


@router.get('/sessions/patient/{patient_id}', response_model=list[SessionResponse])
def list_sessions_for_patient(patient_id: str) -> list[SessionResponse]:
    try:
        response = supabase.table('sessions').select('*').eq('patient_id', patient_id).order('date', desc=True).execute()
        return [_session_from_row(row) for row in response.data or []]
    except Exception as exc:
        print(f'Error fetching sessions for patient {patient_id}: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to fetch sessions: {exc}') from exc


@router.delete('/sessions/{session_id}')
def delete_session(session_id: str) -> dict[str, str]:
    try:
        supabase.table('sessions').delete().eq('id', session_id).execute()
        return {'message': 'Session deleted'}
    except Exception as exc:
        print(f'Error deleting session {session_id}: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to delete session: {exc}') from exc
