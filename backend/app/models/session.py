from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

RiskLevel = Literal['LOW', 'MEDIUM', 'HIGH']


class SessionCreate(BaseModel):
    patient_id: str = Field(min_length=1)
    exercise: str = Field(min_length=1)


class SessionResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    patient_id: str
    patient_name: str
    exercise: str
    date: str
    risk_level: RiskLevel
    form_score: float
    reps_analysed: int
    avg_knee_angle: float
    confidence: float
    diagnosis: str
    prescription: str
    kinematics: str
    detected_issues: list[str]
    references: list[str]
    chart_data: list[dict]


class AnalysisRequest(BaseModel):
    patient_id: str = Field(min_length=1)
    exercise: str = Field(min_length=1)


class AnalysisResponse(BaseModel):
    session: SessionResponse
    message: str


def new_session_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
