"""Appointment business logic.

Handles booking, cancellation, and rescheduling requests.
All methods validate input, generate deterministic identifiers,
and return response schemas.

Booking persistence is delegated to :mod:`GoogleSheetsService`.
When Google Sheets is configured, persistence occurs **before**
the API reports success.  A failed write prevents a success
response from being returned.
"""

import hashlib
import logging
from datetime import datetime, timezone

from app.models.domain import (
    SERVICE_DISPLAY_NAMES,
    DentalService,
    MSG_BOOKING_SUCCESS,
    MSG_CANCEL_SUCCESS,
    MSG_RESCHEDULE_SUCCESS,
)
from app.schemas.appointments import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse,
)
from app.services.google_sheets_service import get_google_sheets_service

logger = logging.getLogger(__name__)


class BookingPersistenceError(Exception):
    """Raised when Google Sheets is enabled but persistence fails.

    This is a domain-level exception — it does not carry HTTP semantics.
    The route handler is responsible for mapping it to an appropriate
    HTTP status and response body.
    """


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

    Orchestration order:
        1. Generate booking ID.
        2. If Google Sheets is enabled → persist the row.
           - On success → proceed to build the response.
           - On failure → raise :class:`BookingPersistenceError`.
        3. If Google Sheets is disabled → log a warning and proceed.
        4. Build and return the success response.

    Raises:
        BookingPersistenceError: If Google Sheets is enabled but the
            append operation failed.
    """
    # ---- Step 1: Generate booking ID & resolve display values ---------------
    booking_id = _generate_id("BK", request.caller_name, request.caller_phone)
    service_name = SERVICE_DISPLAY_NAMES.get(
        request.selected_service, request.selected_service.value
    )
    preferred_date_str = request.preferred_date.isoformat()
    preferred_time_str = request.preferred_time.strftime("%H:%M")

    logger.info(
        "Booking request validated — id=%s name=%s phone=%s service=%s date=%s time=%s",
        booking_id,
        request.caller_name,
        request.caller_phone,
        service_name,
        preferred_date_str,
        preferred_time_str,
    )

    # ---- Step 2: Persist BEFORE reporting success --------------------------
    sheets = get_google_sheets_service()

    if sheets.is_enabled:
        logger.info("Persisting booking to Google Sheets — id=%s", booking_id)
        persisted = sheets.append_booking_row(
            booking_id=booking_id,
            caller_name=request.caller_name,
            caller_phone=request.caller_phone,
            caller_email=request.caller_email or "",
            selected_service=service_name,
            preferred_date=preferred_date_str,
            preferred_time=preferred_time_str,
        )
        if not persisted:
            logger.error(
                "Booking persistence failed — id=%s — "
                "will NOT report success to caller",
                booking_id,
            )
            raise BookingPersistenceError(
                f"Failed to persist booking {booking_id} to Google Sheets. "
                f"The appointment was not recorded."
            )
    else:
        logger.warning(
            "Google Sheets disabled — booking %s accepted without persistence",
            booking_id,
        )

    # ---- Step 3: Send confirmation email (only if persist succeeded) -------
    from app.services.email_service import get_email_service
    if request.caller_email:
        email_service = get_email_service()
        email_service.send_booking_confirmation(
            booking_id=booking_id,
            caller_name=request.caller_name,
            caller_email=request.caller_email,
            selected_service=service_name,
            preferred_date=preferred_date_str,
            preferred_time=preferred_time_str,
        )

    # ---- Step 4: Build success response ------------------------------------
    logger.info("Booking confirmed — id=%s", booking_id)

    return BookAppointmentResponse(
        success=True,
        message=MSG_BOOKING_SUCCESS.format(name=request.caller_name),
        booking_id=booking_id,
        caller_name=request.caller_name,
        caller_phone=request.caller_phone,
        selected_service=service_name,
        preferred_date=preferred_date_str,
        preferred_time=preferred_time_str,
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
        message=MSG_CANCEL_SUCCESS.format(name=request.caller_name),
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
        message=MSG_RESCHEDULE_SUCCESS.format(
            name=request.caller_name,
            date=request.new_date.isoformat(),
            time=request.new_time.strftime('%H:%M')
        ),
        caller_name=request.caller_name,
        caller_phone=request.caller_phone,
        new_date=request.new_date.isoformat(),
        new_time=request.new_time.strftime("%H:%M"),
    )


