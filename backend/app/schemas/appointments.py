"""Request and response schemas for the appointments endpoints."""

from datetime import date, time

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.domain import DentalService
from app.schemas.base import BaseResponse
from app.utils.validators import (
    validate_appointment_date,
    validate_appointment_time,
    validate_indian_phone,
)


# ---- Booking ---------------------------------------------------------------


class BookAppointmentRequest(BaseModel):
    """Payload sent by RetellAI when the caller confirms an appointment."""

    caller_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the caller.",
        examples=["Rahul Sharma"],
    )
    caller_phone: str = Field(
        ...,
        description="10-digit Indian mobile number.",
        examples=["9876543210"],
    )
    caller_email: str | None = Field(
        default=None,
        description="Email address (optional). Validated if provided.",
        examples=["rahul@gmail.com"],
    )
    selected_service: DentalService = Field(
        ...,
        description="Dental service the caller selected.",
        examples=["teeth_whitening"],
    )
    preferred_date: date = Field(
        ...,
        description="Preferred appointment date (YYYY-MM-DD).",
        examples=["2026-07-10"],
    )
    preferred_time: time = Field(
        ...,
        description="Preferred appointment time (HH:MM, 24-hour).",
        examples=["11:00"],
    )

    @field_validator("caller_phone")
    @classmethod
    def _validate_phone(cls, value: str) -> str:
        return validate_indian_phone(value)

    @field_validator("caller_email")
    @classmethod
    def _validate_email(cls, value: str | None) -> str | None:
        if value is None or value.strip() == "":
            return None
        # Light-weight check: pydantic's EmailStr would add a dep;
        # keep it regex-lean for now.
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email address format.")
        return value.strip().lower()

    @field_validator("preferred_date")
    @classmethod
    def _validate_date(cls, value: date) -> date:
        return validate_appointment_date(value)

    @field_validator("preferred_time")
    @classmethod
    def _validate_time(cls, value: time) -> time:
        return validate_appointment_time(value)


class BookAppointmentResponse(BaseResponse):
    """Returned after a successful booking request."""

    booking_id: str = Field(
        ...,
        description="Unique identifier for the booking.",
        examples=["BK-20260710-A1B2"],
    )
    caller_name: str
    caller_phone: str
    selected_service: str
    preferred_date: str
    preferred_time: str


# ---- Cancellation ----------------------------------------------------------


class CancelAppointmentRequest(BaseModel):
    """Payload sent by RetellAI when the caller wants to cancel."""

    caller_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name the appointment was booked under.",
        examples=["Priya Desai"],
    )
    caller_phone: str = Field(
        ...,
        description="Phone number the appointment was booked under.",
        examples=["9988776655"],
    )
    cancel_reason: str | None = Field(
        default=None,
        max_length=500,
        description="Optional reason for cancellation.",
        examples=["Something came up."],
    )

    @field_validator("caller_phone")
    @classmethod
    def _validate_phone(cls, value: str) -> str:
        return validate_indian_phone(value)


class CancelAppointmentResponse(BaseResponse):
    """Returned after a successful cancellation request."""

    caller_name: str
    caller_phone: str


# ---- Rescheduling ----------------------------------------------------------


class RescheduleAppointmentRequest(BaseModel):
    """Payload sent by RetellAI when the caller wants to reschedule."""

    caller_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Name the appointment was booked under.",
        examples=["Amit Joshi"],
    )
    caller_phone: str = Field(
        ...,
        description="Phone number the appointment was booked under.",
        examples=["8877665544"],
    )
    new_date: date = Field(
        ...,
        description="New preferred date (YYYY-MM-DD).",
        examples=["2026-07-15"],
    )
    new_time: time = Field(
        ...,
        description="New preferred time (HH:MM, 24-hour).",
        examples=["15:00"],
    )

    @field_validator("caller_phone")
    @classmethod
    def _validate_phone(cls, value: str) -> str:
        return validate_indian_phone(value)

    @field_validator("new_date")
    @classmethod
    def _validate_date(cls, value: date) -> date:
        return validate_appointment_date(value)

    @field_validator("new_time")
    @classmethod
    def _validate_time(cls, value: time) -> time:
        return validate_appointment_time(value)


class RescheduleAppointmentResponse(BaseResponse):
    """Returned after a successful rescheduling request."""

    caller_name: str
    caller_phone: str
    new_date: str
    new_time: str
