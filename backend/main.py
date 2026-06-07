from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import health_check_supabase
from app.routers.analysis import router as analysis_router
from app.routers.patients import router as patients_router
from app.routers.sessions import router as sessions_router
from app.services.groq_service import is_groq_available
from app.services.inference import is_model_loaded
from app.services.mediapipe_service import is_mediapipe_available


app = FastAPI(title=settings.api_title, version=settings.api_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(patients_router, prefix='/api')
app.include_router(sessions_router, prefix='/api')
app.include_router(analysis_router, prefix='/api')


@app.get('/')
def root() -> dict[str, str]:
    return {'status': 'IntentFlow API running', 'version': settings.api_version}


@app.get('/health')
def health() -> dict[str, object]:
    return {
        'status': 'healthy',
        'version': settings.api_version,
        'supabase': health_check_supabase(),
        'model_loaded': is_model_loaded(),
        'mediapipe_ready': is_mediapipe_available(),
        'groq_ready': is_groq_available(),
    }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
