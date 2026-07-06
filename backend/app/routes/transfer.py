"""Human-transfer webhook endpoint consumed by RetellAI."""

import logging

from fastapi import APIRouter

from app.schemas.transfer import HumanTransferRequest, HumanTransferResponse
from app.services import transfer_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Transfer"])


@router.post(
    "/human-transfer",
    response_model=HumanTransferResponse,
    summary="Request a human transfer",
    description=(
        "Logs the transfer event and returns the clinic front-desk phone "
        "number for RetellAI to execute the warm handoff. Called by the "
        "RetellAI ``node_human_transfer`` Function Node."
    ),
)
async def human_transfer(request: HumanTransferRequest) -> HumanTransferResponse:
    """Log and initiate a transfer to a human agent."""
    logger.info("POST /human-transfer — reason=%s", request.reason)
    return transfer_service.request_human_transfer(request)
