"""Email service for sending booking confirmations.

Encapsulates all email generation and SMTP delivery logic.

Lifecycle
---------
1. On first use, the service checks if SMTP credentials are configured.
2. If configured, it formats and sends a confirmation email.
3. If not configured, it operates in disabled mode, logging a warning and skipping the send.
"""

import logging
import smtplib
import ssl
from email.message import EmailMessage

from app.config import get_settings
from app.models.domain import CLINIC_NAME, CLINIC_PHONE, WORKING_DAYS, WORKING_HOURS_END, WORKING_HOURS_START

logger = logging.getLogger(__name__)


class EmailService:
    """Manages the generation and delivery of emails."""

    def __init__(self) -> None:
        self._enabled: bool = False
        self._initialised: bool = False

    def initialise(self) -> None:
        """Check SMTP configuration and enable the service if valid."""
        if self._initialised:
            return

        settings = get_settings()

        if not (
            settings.smtp_host
            and settings.smtp_username
            and settings.smtp_password
            and settings.smtp_from_email
        ):
            logger.warning(
                "Email service disabled — SMTP_HOST, SMTP_USERNAME, SMTP_PASSWORD, or SMTP_FROM_EMAIL not configured"
            )
            self._initialised = True
            return

        self._enabled = True
        logger.info(
            "Email service enabled — host=%s port=%s from_email=%s",
            settings.smtp_host,
            settings.smtp_port,
            settings.smtp_from_email,
        )
        self._initialised = True

    @property
    def is_enabled(self) -> bool:
        """Whether the email service is enabled and configured."""
        return self._enabled

    def send_booking_confirmation(
        self,
        booking_id: str,
        caller_name: str,
        caller_email: str,
        selected_service: str,
        preferred_date: str,
        preferred_time: str,
    ) -> None:
        """Generate and send a booking confirmation email.

        If the service is disabled or an error occurs during delivery,
        the error is logged but not propagated.
        """
        if not self._enabled:
            logger.warning("Email service disabled — confirmation for %s not sent", booking_id)
            return

        if not caller_email:
            logger.info("No email provided for booking %s — skipping confirmation email", booking_id)
            return

        settings = get_settings()

        msg = EmailMessage()
        msg["Subject"] = f"Appointment Confirmation – {CLINIC_NAME}"
        msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>" if settings.smtp_from_name else settings.smtp_from_email
        msg["To"] = caller_email

        body = (
            f"Dear {caller_name},\n\n"
            f"Your appointment has been successfully booked.\n\n"
            f"Booking Details:\n"
            f"- Booking ID: {booking_id}\n"
            f"- Service: {selected_service}\n"
            f"- Date: {preferred_date}\n"
            f"- Time: {preferred_time}\n\n"
            f"Clinic Details:\n"
            f"- Name: {CLINIC_NAME}\n"
            f"- Working Hours: {WORKING_DAYS}, {WORKING_HOURS_START.strftime('%I:%M %p')} to {WORKING_HOURS_END.strftime('%I:%M %p')}\n"
            f"- Support Contact: {CLINIC_PHONE}\n\n"
            f"Thank you for choosing us.\n"
            f"Regards,\n"
            f"{CLINIC_NAME}"
        )
        msg.set_content(body)

        logger.info("Generating confirmation email for booking %s to %s", booking_id, caller_email)

        try:
            context = ssl.create_default_context()
            logger.info("Connecting to SMTP server %s:%s", settings.smtp_host, settings.smtp_port)
            
            with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(settings.smtp_username, settings.smtp_password)
                server.send_message(msg)
                
            logger.info("Confirmation email sent successfully for booking %s", booking_id)
        except Exception:
            logger.exception("Failed to send confirmation email for booking %s", booking_id)


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_instance: EmailService | None = None


def get_email_service() -> EmailService:
    """Return the module-level singleton, creating it on first call."""
    global _instance
    if _instance is None:
        _instance = EmailService()
        _instance.initialise()
    return _instance
