"""Clinic-information read endpoints."""

import logging
from datetime import date

from fastapi import APIRouter, Query

from app.schemas.clinic import AvailabilityResponse, ServicesResponse
from app.services import clinic_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Clinic"])


@router.get(
    "/services",
    response_model=ServicesResponse,
    summary="List dental services",
    description="Returns all dental services offered by QuensultingAI Dental Clinic.",
)
async def list_services() -> ServicesResponse:
    """Return the full catalogue of dental services."""
    logger.info("GET /services")
    return clinic_service.get_services()


@router.get(
    "/availability",
    response_model=AvailabilityResponse,
    summary="Check appointment availability",
    description=(
        "Returns hourly time slots for a given date, indicating "
        "whether each slot is available for booking."
    ),
)
async def check_availability(
    query_date: date = Query(
        alias="date",
        description="Date to check in YYYY-MM-DD format.",
        examples=["2026-07-10"],
    ),
) -> AvailabilityResponse:
    """Return time-slot availability for a given date."""
    logger.info("GET /availability — date=%s", query_date.isoformat())
    return clinic_service.get_availability(query_date)
