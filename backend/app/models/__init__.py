"""Domain models sub-package — enumerations, constants, and shared types."""

from app.models.domain import (
    CLINIC_LOCATION,
    CLINIC_NAME,
    CLINIC_PHONE,
    CONSULTATION_FEE_INR,
    PAYMENT_METHODS,
    SERVICE_DISPLAY_NAMES,
    WORKING_DAYS,
    WORKING_HOURS_END,
    WORKING_HOURS_START,
    DentalService,
    TransferReason,
)

__all__ = [
    "CLINIC_LOCATION",
    "CLINIC_NAME",
    "CLINIC_PHONE",
    "CONSULTATION_FEE_INR",
    "DentalService",
    "PAYMENT_METHODS",
    "SERVICE_DISPLAY_NAMES",
    "TransferReason",
    "WORKING_DAYS",
    "WORKING_HOURS_END",
    "WORKING_HOURS_START",
]
