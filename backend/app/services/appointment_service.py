"""Appointment business logic.

Handles booking, cancellation, and rescheduling requests.
All methods validate input, generate deterministic identifiers,
and return response schemas.  Persistence will be added in a
future phase (Google Sheets / database).
"""

import hashlib
import logging
from datetime import datetime, timezone

from app.models.domain import SERVICE_DISPLAY_NAMES, DentalService
from app.schemas.appointments import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse,
)

logger = logging.getLogger(__name__)


def _generate_id(prefix: str, *parts: str) -> str:
    """Generate a short deterministic identifier.

    Uses a hash of the input parts combined with the current UTC
    timestamp to produce a human-friendly ID such as ``BK-20260710-A1B2``.
    """
    now = datetime.now(tz=timezone.utc)
    date_segment = now.strftime("%Y%m%d")
    raw = f"{prefix}-{'-'.join(parts)}-{now.isoformat()}"
    hash_segment = hashlib.sha256(raw.encode()).hexdigest()[:4].upper()
    return f"{prefix}-{date_segment}-{hash_segment}"


def book_appointment(request: BookAppointmentRequest) -> BookAppointmentResponse:
    """Process an appointment booking request.

    Generates a booking ID and returns a confirmation response.
    The actual persistence (e.g. Google Sheets row insert) will
    be injected here in a future phase.
    """
    booking_id = _generate_id("BK", request.caller_name, request.caller_phone)
    service_name = SERVICE_DISPLAY_NAMES.get(
        request.selected_service, request.selected_service.value
    )

    logger.info(
        "Appointment booked — id=%s name=%s phone=%s service=%s date=%s time=%s",
        booking_id,
        request.caller_name,
        request.caller_phone,
        service_name,
        request.preferred_date.isoformat(),
        request.preferred_time.strftime("%H:%M"),
    )

    return BookAppointmentResponse(
        success=True,
        message=f"Appointment booked successfully for {request.caller_name}.",
        booking_id=booking_id,
        caller_name=request.caller_name,
        caller_phone=request.caller_phone,
        selected_service=service_name,
        preferred_date=request.preferred_date.isoformat(),
        preferred_time=request.preferred_time.strftime("%H:%M"),
    )


def cancel_appointment(request: CancelAppointmentRequest) -> CancelAppointmentResponse:
    """Process an appointment cancellation request.

    Logs the cancellation and returns a confirmation.  Actual
    record deletion / status update will be added in a future phase.
    """
    logger.info(
        "Appointment cancelled — name=%s phone=%s reason=%s",
        request.caller_name,
        request.caller_phone,
        request.cancel_reason or "not provided",
    )

    return CancelAppointmentResponse(
        success=True,
        message=f"Appointment for {request.caller_name} has been cancelled.",
        caller_name=request.caller_name,
        caller_phone=request.caller_phone,
    )


def reschedule_appointment(
    request: RescheduleAppointmentRequest,
) -> RescheduleAppointmentResponse:
    """Process an appointment rescheduling request.

    Logs the reschedule and returns a confirmation with the new
    date and time.  Actual record update will be added in a future phase.
    """
    logger.info(
        "Appointment rescheduled — name=%s phone=%s new_date=%s new_time=%s",
        request.caller_name,
        request.caller_phone,
        request.new_date.isoformat(),
        request.new_time.strftime("%H:%M"),
    )

    return RescheduleAppointmentResponse(
        success=True,
        message=(
            f"Appointment for {request.caller_name} has been rescheduled to "
            f"{request.new_date.isoformat()} at {request.new_time.strftime('%H:%M')}."
        ),
        caller_name=request.caller_name,
        caller_phone=request.caller_phone,
        new_date=request.new_date.isoformat(),
        new_time=request.new_time.strftime("%H:%M"),
    )
