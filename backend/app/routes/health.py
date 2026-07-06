"""Health-check endpoint."""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the current health status of the service.",
)
async def health_check() -> HealthResponse:
    """Return a simple health-check payload."""
    return HealthResponse(status="healthy")
