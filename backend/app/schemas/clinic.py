"""Response schemas for the clinic-information read endpoints."""

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class ServiceItem(BaseModel):
    """A single dental service offered by the clinic."""

    key: str = Field(..., description="Machine-readable service identifier.")
    display_name: str = Field(..., description="Human-readable service name.")


class ServicesResponse(BaseResponse):
    """Returned by ``GET /services``."""

    services: list[ServiceItem]


class TimeSlot(BaseModel):
    """A single available time slot."""

    time: str = Field(..., description="Slot time in HH:MM format.", examples=["09:00"])
    available: bool = Field(..., description="Whether the slot is bookable.")


class AvailabilityResponse(BaseResponse):
    """Returned by ``GET /availability``."""

    date: str = Field(..., description="The queried date (YYYY-MM-DD).")
    day: str = Field(..., description="Day of the week.")
    clinic_open: bool
    slots: list[TimeSlot]
