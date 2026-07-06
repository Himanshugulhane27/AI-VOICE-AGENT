"""Shared base response schema used by all API endpoints."""

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """Standard envelope for every API response.

    Provides a consistent shape that RetellAI Function Nodes can
    rely on when mapping response fields to dynamic variables.
    """

    success: bool
    message: str
    request_id: str | None = None
