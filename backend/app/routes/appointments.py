"""Appointment webhook endpoints consumed by RetellAI Function Nodes."""

import logging

from fastapi import APIRouter

from app.schemas.appointments import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse,
)
from app.services import appointment_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post(
    "/book",
    response_model=BookAppointmentResponse,
    summary="Book a new appointment",
    description=(
        "Validates caller details and the selected service, date, and time, "
        "then returns a booking confirmation with a unique booking ID. "
        "Called by the RetellAI ``node_booking_api`` Function Node."
    ),
)
async def book(request: BookAppointmentRequest) -> BookAppointmentResponse:
    """Book a new dental appointment."""
    logger.info("POST /appointments/book — caller=%s", request.caller_name)
    return appointment_service.book_appointment(request)


@router.post(
    "/cancel",
    response_model=CancelAppointmentResponse,
    summary="Cancel an existing appointment",
    description=(
        "Looks up the appointment by name and phone, then marks it as "
        "cancelled. Called by the RetellAI ``node_cancel_api`` Function Node."
    ),
)
async def cancel(request: CancelAppointmentRequest) -> CancelAppointmentResponse:
    """Cancel an existing appointment."""
    logger.info("POST /appointments/cancel — caller=%s", request.caller_name)
    return appointment_service.cancel_appointment(request)


@router.post(
    "/reschedule",
    response_model=RescheduleAppointmentResponse,
    summary="Reschedule an existing appointment",
    description=(
        "Updates the appointment date and time. Called by the RetellAI "
        "``node_reschedule_api`` Function Node."
    ),
)
async def reschedule(
    request: RescheduleAppointmentRequest,
) -> RescheduleAppointmentResponse:
    """Reschedule an existing appointment."""
    logger.info("POST /appointments/reschedule — caller=%s", request.caller_name)
    return appointment_service.reschedule_appointment(request)
