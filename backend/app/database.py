from __future__ import annotations

from typing import Any

try:
    from supabase import Client, create_client
except Exception:  # pragma: no cover - import-time fallback for partial environments
    Client = Any  # type: ignore[assignment]
    create_client = None  # type: ignore[assignment]

from .config import settings

if create_client is not None:
    supabase: Client | Any = create_client(settings.supabase_url, settings.supabase_key)
else:
    supabase = None


def health_check_supabase() -> dict[str, Any]:
    if supabase is None:
        return {
            'connected': False,
            'message': 'Supabase client unavailable',
        }

    try:
        response = supabase.table('patients').select('id').limit(1).execute()
        return {
            'connected': True,
            'message': 'Supabase connection healthy',
            'sample_count': len(response.data or []),
        }
    except Exception as exc:
        print(f'Supabase health check failed: {exc}')
        return {
            'connected': False,
            'message': str(exc),
        }
