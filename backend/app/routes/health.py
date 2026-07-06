"""Health-check endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.email_service import get_email_service
from app.services.google_sheets_service import get_google_sheets_service

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the current health status of the service and its integrations.",
)
async def health_check() -> HealthResponse:
    """Return a comprehensive health-check payload."""
    return HealthResponse(
        status="healthy",
        environment="production",
        version="0.2.0",
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        google_sheets_status="enabled" if get_google_sheets_service().is_enabled else "disabled",
        smtp_status="enabled" if get_email_service().is_enabled else "disabled",
    )
