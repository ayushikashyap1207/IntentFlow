from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from ..database import supabase
from ..models.patient import PatientCreate, PatientDetailResponse, PatientResponse
from ..models.session import SessionResponse

router = APIRouter()


def _risk_rank(risk_level: str | None) -> int:
    order = {'LOW': 0, 'MEDIUM': 1, 'HIGH': 2}
    return order.get((risk_level or 'LOW').upper(), 0)


def _derive_patient_risk(row: dict, sessions: list[dict]) -> str:
    if row.get('risk_level'):
        return str(row['risk_level']).upper()
    if not sessions:
        return 'LOW'
    highest = max(sessions, key=lambda session: _risk_rank(str(session.get('risk_level', 'LOW'))))
    return str(highest.get('risk_level', 'LOW')).upper()


def _patient_to_response(row: dict, sessions: list[dict] | None = None) -> PatientResponse:
    session_rows = sessions or []
    return PatientResponse(
        id=str(row['id']),
        name=str(row['name']),
        age=int(row['age']),
        gender=str(row['gender']),
        condition=str(row['condition']),
        risk_level=_derive_patient_risk(row, session_rows),
        since=str(row['since']),
        created_at=str(row.get('created_at', datetime.now(timezone.utc).isoformat())),
    )


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


@router.get('/patients', response_model=list[PatientResponse])
def list_patients() -> list[PatientResponse]:
    try:
        response = supabase.table('patients').select('*').order('created_at', desc=True).execute()
        patients = response.data or []
        results: list[PatientResponse] = []
        for row in patients:
            session_response = supabase.table('sessions').select('id, risk_level').eq('patient_id', row['id']).execute()
            results.append(_patient_to_response(row, session_response.data or []))
        return results
    except Exception as exc:
        print(f'Error listing patients: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to list patients: {exc}') from exc


@router.get('/patients/{patient_id}', response_model=PatientDetailResponse)
def get_patient(patient_id: str) -> PatientDetailResponse:
    try:
        patient_response = supabase.table('patients').select('*').eq('id', patient_id).limit(1).execute()
        if not patient_response.data:
            raise HTTPException(status_code=404, detail='Patient not found')

        sessions_response = supabase.table('sessions').select('*').eq('patient_id', patient_id).order('date', desc=True).execute()
        sessions = sessions_response.data or []
        patient = _patient_to_response(patient_response.data[0], sessions)
        return PatientDetailResponse(**patient.model_dump(), sessions=[_session_from_row(session).model_dump() for session in sessions])
    except HTTPException:
        raise
    except Exception as exc:
        print(f'Error fetching patient {patient_id}: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to fetch patient: {exc}') from exc


@router.post('/patients', response_model=PatientResponse, status_code=201)
def create_patient(payload: PatientCreate) -> PatientResponse:
    try:
        now = datetime.now(timezone.utc).isoformat()
        patient_id = str(uuid4())
        row = {
            'id': patient_id,
            'name': payload.name,
            'age': payload.age,
            'gender': payload.gender,
            'condition': payload.condition,
            'since': payload.since,
            'risk_level': 'LOW',
            'created_at': now,
        }
        response = supabase.table('patients').insert(row).execute()
        saved_row = (response.data or [row])[0]
        return _patient_to_response(saved_row, [])
    except Exception as exc:
        print(f'Error creating patient: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to create patient: {exc}') from exc


@router.delete('/patients/{patient_id}')
def delete_patient(patient_id: str) -> dict[str, str]:
    try:
        supabase.table('sessions').delete().eq('patient_id', patient_id).execute()
        supabase.table('patients').delete().eq('id', patient_id).execute()
        return {'message': 'Patient deleted'}
    except Exception as exc:
        print(f'Error deleting patient {patient_id}: {exc}')
        raise HTTPException(status_code=500, detail=f'Failed to delete patient: {exc}') from exc
