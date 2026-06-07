from __future__ import annotations

import json
from typing import Any

try:
    from groq import Groq
except Exception:  # pragma: no cover - import-time fallback for partial environments
    Groq = None  # type: ignore[assignment]

from ..config import settings
from ..core.diagnostics import get_fallback_report


def is_groq_available() -> bool:
    return bool(settings.groq_api_key and Groq is not None)


def _validate_report(payload: dict[str, Any], exercise: str) -> dict[str, Any]:
    report = get_fallback_report(exercise)
    report.update(
        {
            'diagnosis': str(payload.get('diagnosis', report['diagnosis'])),
            'prescription': str(payload.get('prescription', report['prescription'])),
            'kinematics': str(payload.get('kinematics', report['kinematics'])),
            'risk_level': payload.get('risk_level', report['risk_level']),
            'detected_issues': list(payload.get('detected_issues', report['detected_issues'])),
            'references': list(payload.get('references', report['references'])),
            'form_score': int(payload.get('form_score', report['form_score'])),
        }
    )
    return report


def generate_clinical_report(exercise: str, predicted_class: str, confidence: float, sequence_stats: dict[str, Any]) -> dict[str, Any]:
    fallback = get_fallback_report(exercise)

    if not settings.groq_api_key or Groq is None:
        return fallback

    try:
        client = Groq(api_key=settings.groq_api_key)
        system_prompt = (
            'You are a senior physiotherapist AI assistant. Given movement analysis data, '
            'generate a structured clinical report. Always respond in valid JSON only.'
        )
        user_prompt = json.dumps(
            {
                'exercise': exercise,
                'predicted_class': predicted_class,
                'confidence': confidence,
                'sequence_stats': sequence_stats,
                'required_schema': {
                    'diagnosis': 'string',
                    'prescription': 'string',
                    'kinematics': 'string',
                    'risk_level': 'LOW|MEDIUM|HIGH',
                    'detected_issues': ['string'],
                    'references': ['string'],
                    'form_score': 'integer 0-100',
                },
            },
            indent=2,
        )

        response = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            temperature=0.2,
            response_format={'type': 'json_object'},
        )

        content = response.choices[0].message.content or '{}'
        payload = json.loads(content)
        return _validate_report(payload, exercise)
    except Exception as exc:
        print(f'Groq generation failed: {exc}')
        return fallback
