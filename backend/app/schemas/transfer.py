"""Request and response schemas for the human-transfer endpoint."""

from pydantic import BaseModel, Field

from app.models.domain import TransferReason
from app.schemas.base import BaseResponse


class HumanTransferRequest(BaseModel):
    """Payload sent by RetellAI when a call should be transferred."""

    reason: TransferReason = Field(
        ...,
        description="Why the transfer is happening.",
        examples=["emergency"],
    )
    caller_name: str | None = Field(
        default=None,
        max_length=100,
        description="Caller name if already collected.",
        examples=["Rahul Sharma"],
    )
    caller_phone: str | None = Field(
        default=None,
        description="Caller phone if already collected.",
        examples=["9876543210"],
    )
    context: str | None = Field(
        default=None,
        max_length=1000,
        description="Additional context for the human agent.",
        examples=["Caller reported severe tooth pain and bleeding."],
    )


class HumanTransferResponse(BaseResponse):
    """Returned after logging the transfer request."""

    transfer_id: str = Field(
        ...,
        description="Unique identifier for the transfer event.",
        examples=["TR-20260710-X1Y2"],
    )
    reason: str
    transfer_target: str = Field(
        ...,
        description="Phone number or destination the call is routed to.",
    )
