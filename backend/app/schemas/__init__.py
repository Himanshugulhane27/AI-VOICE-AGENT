"""Pydantic schemas sub-package — request / response contracts."""

from app.schemas.appointments import (
    BookAppointmentRequest,
    BookAppointmentResponse,
    CancelAppointmentRequest,
    CancelAppointmentResponse,
    RescheduleAppointmentRequest,
    RescheduleAppointmentResponse,
)
from app.schemas.base import BaseResponse
from app.schemas.clinic import AvailabilityResponse, ServiceItem, ServicesResponse, TimeSlot
from app.schemas.faq import FaqRequest, FaqResponse
from app.schemas.health import HealthResponse
from app.schemas.transfer import HumanTransferRequest, HumanTransferResponse

__all__ = [
    "AvailabilityResponse",
    "BaseResponse",
    "BookAppointmentRequest",
    "BookAppointmentResponse",
    "CancelAppointmentRequest",
    "CancelAppointmentResponse",
    "FaqRequest",
    "FaqResponse",
    "HealthResponse",
    "HumanTransferRequest",
    "HumanTransferResponse",
    "RescheduleAppointmentRequest",
    "RescheduleAppointmentResponse",
    "ServiceItem",
    "ServicesResponse",
    "TimeSlot",
]
