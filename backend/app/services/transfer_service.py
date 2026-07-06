"""Human-transfer business logic.

Logs the transfer event and returns the transfer target for
RetellAI to execute the warm handoff.
"""

import logging
from datetime import datetime, timezone
import hashlib

from app.models.domain import CLINIC_PHONE
from app.schemas.transfer import HumanTransferRequest, HumanTransferResponse

logger = logging.getLogger(__name__)


def request_human_transfer(request: HumanTransferRequest) -> HumanTransferResponse:
    """Process a human-transfer request.

    Generates a transfer event ID, logs all available context, and
    returns the clinic front-desk number as the transfer target.
    """
    now = datetime.now(tz=timezone.utc)
    date_segment = now.strftime("%Y%m%d")
    raw = f"TR-{request.reason}-{now.isoformat()}"
    hash_segment = hashlib.sha256(raw.encode()).hexdigest()[:4].upper()
    transfer_id = f"TR-{date_segment}-{hash_segment}"

    logger.info(
        "Human transfer requested — id=%s reason=%s caller_name=%s caller_phone=%s context=%s",
        transfer_id,
        request.reason,
        request.caller_name or "unknown",
        request.caller_phone or "unknown",
        request.context or "none",
    )

    return HumanTransferResponse(
        success=True,
        message="Call is being transferred to the front desk.",
        transfer_id=transfer_id,
        reason=request.reason.value,
        transfer_target=CLINIC_PHONE,
    )
