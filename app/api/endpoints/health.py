"""Health-check endpoint."""

from fastapi import APIRouter

from app.api.dependencies import SettingsDep
from app.schemas.common import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse, summary="Service health check")
def health_check(settings: SettingsDep) -> HealthResponse:
    return HealthResponse(status="ok", app_name=settings.app_name, version=settings.app_version)
