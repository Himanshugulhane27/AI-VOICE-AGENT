"""FAQ business logic.

Matches caller questions to a curated knowledge base of clinic
information.  Keyword-based matching is used intentionally — the
RetellAI conversation flow already handles NLU; this endpoint
serves as a structured fallback for Function Node calls.
"""

import logging

from app.schemas.faq import FaqRequest, FaqResponse

logger = logging.getLogger(__name__)

# ---- Knowledge base --------------------------------------------------------
# Each entry: (category, keywords, answer)

_FAQ_ENTRIES: list[tuple[str, list[str], str]] = [
    (
        "working_hours",
        ["timing", "timings", "hours", "open", "close", "when", "schedule"],
        "We are open Monday to Saturday, 9 AM to 6 PM. We are closed on Sundays.",
    ),
    (
        "location",
        ["location", "address", "where", "directions", "map", "baner", "pune"],
        "We are located in Baner, Pune.",
    ),
    (
        "consultation_fee",
        ["fee", "fees", "cost", "charge", "price", "consultation", "how much"],
        "The consultation fee is ₹500.",
    ),
    (
        "payment_methods",
        ["payment", "pay", "upi", "cash", "card", "credit", "debit"],
        "We accept Cash, UPI, Credit Card, and Debit Card.",
    ),
    (
        "walk_ins",
        ["walk-in", "walk in", "walkin", "without appointment", "directly"],
        "Walk-ins are accepted, but we recommend booking an appointment to avoid waiting.",
    ),
    (
        "emergency",
        ["emergency", "urgent", "pain", "bleeding", "swelling"],
        "Emergency appointments are subject to doctor availability. "
        "Please call us immediately and we will try to accommodate you.",
    ),
    (
        "services",
        ["service", "services", "treatment", "treatments", "offer", "provide", "do you do"],
        "We offer Dental Cleaning, Root Canal Treatment, Teeth Whitening, "
        "Braces Consultation, Tooth Extraction, and General Dental Consultation.",
    ),
]

_DEFAULT_ANSWER = (
    "general",
    "I'm not sure about that. I can connect you with our front desk "
    "for more detailed information.",
)


def answer_faq(request: FaqRequest) -> FaqResponse:
    """Match the caller's question to the knowledge base and return an answer.

    Performs case-insensitive keyword matching against the question text.
    Returns the first matching entry, or a default fallback if no keywords match.
    """
    question_lower = request.question.lower()

    for category, keywords, answer in _FAQ_ENTRIES:
        if any(kw in question_lower for kw in keywords):
            logger.info(
                "FAQ matched — category=%s question=%s",
                category,
                request.question,
            )
            return FaqResponse(
                success=True,
                message="FAQ answered.",
                question=request.question,
                answer=answer,
                category=category,
            )

    logger.info("FAQ unmatched — question=%s", request.question)
    return FaqResponse(
        success=True,
        message="No exact match found. Returning general response.",
        question=request.question,
        answer=_DEFAULT_ANSWER[1],
        category=_DEFAULT_ANSWER[0],
    )
