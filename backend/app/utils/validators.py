"""Pydantic validators reused across multiple schemas."""

import re
from datetime import date, time

from app.models.domain import WORKING_DAYS, WORKING_HOURS_END, WORKING_HOURS_START

# Indian mobile: starts with 6-9, exactly 10 digits.
_INDIAN_PHONE_RE = re.compile(r"^[6-9]\d{9}$")


def validate_indian_phone(value: str) -> str:
    """Strip common prefixes and validate a 10-digit Indian mobile number.

    Accepts formats like ``+919876543210``, ``09876543210``, or
    ``9876543210``.  Returns the bare 10-digit string.

    Raises:
        ValueError: If the number is not a valid Indian mobile number.
    """
    cleaned = re.sub(r"[\s\-()]", "", value)
    if cleaned.startswith("+91"):
        cleaned = cleaned[3:]
    elif cleaned.startswith("91") and len(cleaned) == 12:
        cleaned = cleaned[2:]
    elif cleaned.startswith("0") and len(cleaned) == 11:
        cleaned = cleaned[1:]

    if not _INDIAN_PHONE_RE.match(cleaned):
        raise ValueError(
            "Phone number must be a valid 10-digit Indian mobile number "
            "starting with 6, 7, 8, or 9."
        )
    return cleaned


def validate_appointment_date(value: date) -> date:
    """Ensure the appointment date is not in the past and falls on a working day.

    Raises:
        ValueError: If the date is in the past or on a Sunday.
    """
    today = date.today()
    if value < today:
        raise ValueError("Appointment date cannot be in the past.")
    day_name = value.strftime("%A")
    if day_name not in WORKING_DAYS:
        raise ValueError(
            f"The clinic is closed on {day_name}. "
            f"Please choose a day from Monday to Saturday."
        )
    return value


def validate_appointment_time(value: time) -> time:
    """Ensure the appointment time is within clinic working hours (9 AM – 6 PM).

    Raises:
        ValueError: If the time is outside working hours.
    """
    if value.hour < WORKING_HOURS_START or value.hour >= WORKING_HOURS_END:
        raise ValueError(
            f"Appointment time must be between "
            f"{WORKING_HOURS_START}:00 AM and {WORKING_HOURS_END - 12}:00 PM."
        )
    return value
