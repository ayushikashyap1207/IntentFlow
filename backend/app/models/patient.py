from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

RiskLevel = Literal['LOW', 'MEDIUM', 'HIGH']


def _compute_initials(name: str) -> str:
    parts = [part for part in name.strip().split() if part]
    if not parts:
        return 'UN'
    first = parts[0][0]
    last = parts[-1][0] if len(parts) > 1 else parts[0][1:2]
    return (first + last).upper()


class PatientCreate(BaseModel):
    name: str = Field(min_length=1)
    age: int = Field(ge=0, le=130)
    gender: str = Field(min_length=1)
    condition: str = Field(min_length=1)
    since: str = Field(min_length=1)


class PatientResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    age: int
    gender: str
    condition: str
    risk_level: RiskLevel
    since: str
    created_at: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def initials(self) -> str:
        return _compute_initials(self.name)


class PatientDetailResponse(PatientResponse):
    sessions: list[dict]


def patient_defaults() -> dict[str, str]:
    now = datetime.now(timezone.utc).isoformat()
    return {'created_at': now}
