"""Request and response schemas for the FAQ endpoint."""

from pydantic import BaseModel, Field

from app.schemas.base import BaseResponse


class FaqRequest(BaseModel):
    """Payload sent by RetellAI when the caller asks a clinic question."""

    question: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="The caller's question, as transcribed by RetellAI.",
        examples=["What are your clinic timings?"],
    )


class FaqResponse(BaseResponse):
    """Returned with the matched answer for the caller's question."""

    question: str
    answer: str
    category: str = Field(
        ...,
        description="Category the question was matched to.",
        examples=["working_hours"],
    )
