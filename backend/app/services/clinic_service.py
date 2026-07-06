"""Clinic-information business logic.

Provides service listings and appointment availability data.
Availability currently returns all slots as open — a future
calendar integration will populate real availability.
"""

import logging
from datetime import date

from app.models.domain import (
    SERVICE_DISPLAY_NAMES,
    WORKING_DAYS,
    WORKING_HOURS_END,
    WORKING_HOURS_START,
    DentalService,
)
from app.schemas.clinic import (
    AvailabilityResponse,
    ServiceItem,
    ServicesResponse,
    TimeSlot,
)

logger = logging.getLogger(__name__)


def get_services() -> ServicesResponse:
    """Return the full list of dental services offered by the clinic."""
    items = [
        ServiceItem(key=service.value, display_name=display)
        for service, display in SERVICE_DISPLAY_NAMES.items()
    ]

    logger.info("Services list requested — count=%d", len(items))

    return ServicesResponse(
        success=True,
        message="Available dental services.",
        services=items,
    )


def get_availability(query_date: date) -> AvailabilityResponse:
    """Return time-slot availability for a given date.

    Validates that the date is a working day, then generates hourly
    slots from clinic open to close.  All slots are currently marked
    as available — a future calendar integration will filter booked
    slots.

    Args:
        query_date: The date to check availability for.
    """
    day_name = query_date.strftime("%A")
    clinic_open = day_name in WORKING_DAYS

    slots: list[TimeSlot] = []
    if clinic_open:
        for hour in range(WORKING_HOURS_START, WORKING_HOURS_END):
            slots.append(
                TimeSlot(time=f"{hour:02d}:00", available=True)
            )

    logger.info(
        "Availability requested — date=%s day=%s open=%s slots=%d",
        query_date.isoformat(),
        day_name,
        clinic_open,
        len(slots),
    )

    return AvailabilityResponse(
        success=True,
        message="Clinic is open." if clinic_open else f"Clinic is closed on {day_name}.",
        date=query_date.isoformat(),
        day=day_name,
        clinic_open=clinic_open,
        slots=slots,
    )
