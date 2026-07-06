"""FAQ webhook endpoint consumed by RetellAI Function Nodes."""

import logging

from fastapi import APIRouter

from app.schemas.faq import FaqRequest, FaqResponse
from app.services import faq_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["FAQ"])


@router.post(
    "/faq",
    response_model=FaqResponse,
    summary="Answer a caller's FAQ",
    description=(
        "Matches the caller's question against the clinic knowledge base "
        "and returns a structured answer. Called by the RetellAI "
        "``node_faq_handler`` when configured as a Function Node fallback."
    ),
)
async def faq(request: FaqRequest) -> FaqResponse:
    """Match a caller question to the clinic knowledge base."""
    logger.info("POST /faq — question=%s", request.question)
    return faq_service.answer_faq(request)
