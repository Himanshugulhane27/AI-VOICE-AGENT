"""Google Sheets integration service.

Encapsulates all interaction with the Google Sheets API via ``gspread``.
No other module should import ``gspread`` or ``google.oauth2`` directly.

Lifecycle
---------
1. On first use (lazy initialisation), the service authenticates using
   a Google Service Account JSON key file and opens the target spreadsheet.
2. It ensures the ``Appointments`` worksheet exists and that the header
   row is present.
3. Each call to :func:`append_booking_row` appends a single row.

If ``GOOGLE_SHEET_ID`` or ``GOOGLE_SERVICE_ACCOUNT_FILE`` are empty,
the service operates in **disabled mode** — all write operations are
skipped with a warning log.  This allows the application to start
and serve requests even without Sheets credentials configured.
"""

import logging
from datetime import datetime, timezone
from typing import Any

import gspread
from google.oauth2.service_account import Credentials

from app.config import get_settings

logger = logging.getLogger(__name__)

# Scopes required by gspread for read/write access.
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_WORKSHEET_NAME = "Appointments"

_HEADERS = [
    "Booking ID",
    "Name",
    "Phone",
    "Email",
    "Service",
    "Appointment Date",
    "Appointment Time",
    "Booking Status",
    "Created At",
]


class GoogleSheetsService:
    """Manages the connection to a single Google Sheets spreadsheet.

    The service is designed as a singleton — one instance is created at
    application startup and shared via dependency injection.
    """

    def __init__(self) -> None:
        self._client: gspread.Client | None = None
        self._spreadsheet: gspread.Spreadsheet | None = None
        self._worksheet: gspread.Worksheet | None = None
        self._enabled: bool = False
        self._initialised: bool = False

    # -- Public API ----------------------------------------------------------

    def initialise(self) -> None:
        """Authenticate and prepare the spreadsheet.

        Safe to call multiple times — subsequent calls are no-ops.
        """
        if self._initialised:
            return

        settings = get_settings()

        if not settings.google_sheet_id or not settings.google_service_account_file:
            logger.warning(
                "Google Sheets integration disabled — "
                "GOOGLE_SHEET_ID or GOOGLE_SERVICE_ACCOUNT_FILE not configured"
            )
            self._initialised = True
            return

        try:
            self._authenticate(settings.google_service_account_file)
            self._open_spreadsheet(settings.google_sheet_id)
            self._ensure_worksheet()
            self._ensure_headers()
            self._enabled = True
            logger.info(
                "Google Sheets connected — spreadsheet=%s worksheet=%s",
                settings.google_sheet_id,
                _WORKSHEET_NAME,
            )
        except Exception:
            logger.exception("Failed to initialise Google Sheets integration")
            self._enabled = False

        self._initialised = True

    def append_booking_row(
        self,
        booking_id: str,
        caller_name: str,
        caller_phone: str,
        caller_email: str,
        selected_service: str,
        preferred_date: str,
        preferred_time: str,
    ) -> bool:
        """Append a booking record to the Appointments worksheet.

        Args:
            booking_id: Unique booking identifier (e.g. ``BK-20260710-A1B2``).
            caller_name: Full name of the caller.
            caller_phone: 10-digit phone number.
            caller_email: Email address (may be empty).
            selected_service: Human-readable service name.
            preferred_date: Date string in ISO format.
            preferred_time: Time string in ``HH:MM`` format.

        Returns:
            ``True`` if the row was appended, ``False`` if Sheets is
            disabled or the append failed.
        """
        if not self._enabled:
            logger.warning("Google Sheets disabled — booking %s not persisted", booking_id)
            return False

        created_at = datetime.now(tz=timezone.utc).isoformat()
        row: list[Any] = [
            booking_id,
            caller_name,
            caller_phone,
            caller_email or "",
            selected_service,
            preferred_date,
            preferred_time,
            "Confirmed",
            created_at,
        ]

        try:
            if self._worksheet is None:
                raise RuntimeError("Worksheet reference is None after initialisation")
            self._worksheet.append_row(row, value_input_option="USER_ENTERED")
            logger.info("Booking appended to Google Sheets — id=%s", booking_id)
            return True
        except Exception:
            logger.exception("Failed to append booking to Google Sheets — id=%s", booking_id)
            return False

    @property
    def is_enabled(self) -> bool:
        """Whether the Sheets integration is active and connected."""
        return self._enabled

    # -- Private helpers -----------------------------------------------------

    def _authenticate(self, service_account_file: str) -> None:
        """Create an authenticated gspread client from the service account key."""
        credentials = Credentials.from_service_account_file(
            service_account_file, scopes=_SCOPES
        )
        self._client = gspread.authorize(credentials)
        logger.info("Google Sheets authenticated via service account")

    def _open_spreadsheet(self, sheet_id: str) -> None:
        """Open the spreadsheet by its ID."""
        if self._client is None:
            raise RuntimeError("Client not authenticated")
        self._spreadsheet = self._client.open_by_key(sheet_id)
        logger.info("Spreadsheet opened — id=%s title=%s", sheet_id, self._spreadsheet.title)

    def _ensure_worksheet(self) -> None:
        """Get or create the Appointments worksheet."""
        if self._spreadsheet is None:
            raise RuntimeError("Spreadsheet not opened")

        try:
            self._worksheet = self._spreadsheet.worksheet(_WORKSHEET_NAME)
            logger.info("Worksheet found — name=%s", _WORKSHEET_NAME)
        except gspread.exceptions.WorksheetNotFound:
            self._worksheet = self._spreadsheet.add_worksheet(
                title=_WORKSHEET_NAME, rows=1000, cols=len(_HEADERS)
            )
            logger.info("Worksheet created — name=%s", _WORKSHEET_NAME)

    def _ensure_headers(self) -> None:
        """Insert the header row if the worksheet is empty or headers are missing."""
        if self._worksheet is None:
            raise RuntimeError("Worksheet reference is None")

        first_row = self._worksheet.row_values(1)
        if first_row == _HEADERS:
            logger.info("Headers already present in worksheet")
            return

        if not first_row:
            self._worksheet.append_row(_HEADERS, value_input_option="RAW")
            logger.info("Headers inserted into worksheet")
        else:
            logger.warning(
                "Unexpected header row in worksheet — expected=%s got=%s",
                _HEADERS,
                first_row,
            )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_instance: GoogleSheetsService | None = None


def get_google_sheets_service() -> GoogleSheetsService:
    """Return the module-level singleton, creating it on first call.

    The service is lazily initialised — the first call triggers
    authentication and spreadsheet setup.  Subsequent calls return
    the same instance.
    """
    global _instance
    if _instance is None:
        _instance = GoogleSheetsService()
        _instance.initialise()
    return _instance
