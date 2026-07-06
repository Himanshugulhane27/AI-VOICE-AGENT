# AI Voice Receptionist — Backend

Production-ready FastAPI backend for the **QuensultingAI Dental Clinic** AI-powered voice receptionist.

## Project Structure

```
backend/
├── main.py                          # CLI entry point (python main.py)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variable template
├── .env                             # Local environment overrides (git-ignored)
├── docs/
│   └── retellai_conversation_flow.md  # Phase 2 — conversation design
└── app/
    ├── __init__.py
    ├── main.py                      # FastAPI application factory
    ├── config/
    │   ├── __init__.py
    │   └── settings.py              # Pydantic Settings (typed env loading)
    ├── routes/
    │   ├── __init__.py
    │   ├── health.py                # GET  /health
    │   ├── appointments.py          # POST /appointments/{book,cancel,reschedule}
    │   ├── faq.py                   # POST /faq
    │   ├── transfer.py              # POST /human-transfer
    │   └── clinic.py                # GET  /services, /availability
    ├── services/
    │   ├── __init__.py
    │   ├── appointment_service.py   # Booking / cancel / reschedule logic
    │   ├── faq_service.py           # FAQ knowledge base matching
    │   ├── transfer_service.py      # Human transfer event logging
    │   ├── clinic_service.py        # Service catalogue & availability
    │   └── google_sheets_service.py # Google Sheets persistence (Phase 3.2)
    ├── models/
    │   ├── __init__.py
    │   └── domain.py                # Enums, constants, clinic metadata
    ├── schemas/
    │   ├── __init__.py
    │   ├── base.py                  # BaseResponse envelope
    │   ├── health.py                # Health response
    │   ├── appointments.py          # Book / cancel / reschedule schemas
    │   ├── faq.py                   # FAQ schemas
    │   ├── transfer.py              # Human transfer schemas
    │   └── clinic.py                # Services / availability schemas
    └── utils/
        ├── __init__.py
        ├── logging.py               # Structured logging configuration
        └── validators.py            # Phone, date, time validation
```

## Quick Start

### 1. Create a virtual environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run the server

**Option A — uvicorn CLI (recommended for development):**

```bash
uvicorn app.main:app --reload
```

**Option B — Python script:**

```bash
python main.py
```

The server starts on `http://0.0.0.0:8000` by default.

### 5. Verify

```bash
curl http://localhost:8000/health
# → {"status":"healthy"}
```

Interactive API docs are available at `http://localhost:8000/docs`.

## API Endpoints

| Method | Path                        | Description                  |
|--------|-----------------------------|------------------------------|
| GET    | `/health`                   | Service health check         |
| GET    | `/services`                 | List dental services         |
| GET    | `/availability?date=...`    | Check time-slot availability |
| POST   | `/appointments/book`        | Book an appointment          |
| POST   | `/appointments/cancel`      | Cancel an appointment        |
| POST   | `/appointments/reschedule`  | Reschedule an appointment    |
| POST   | `/faq`                      | Answer a caller's question   |
| POST   | `/human-transfer`           | Request human agent transfer |

## Configuration

All configuration is loaded from environment variables (or a `.env` file) via **pydantic-settings**.

| Variable                       | Default   | Description                            |
|--------------------------------|-----------|----------------------------------------|
| `HOST`                         | `0.0.0.0` | Server bind address                    |
| `PORT`                         | `8000`    | Server bind port                       |
| `LOG_LEVEL`                    | `info`    | Logging verbosity                      |
| `GOOGLE_SHEET_ID`              | —         | Google Sheets spreadsheet ID           |
| `GOOGLE_SERVICE_ACCOUNT_FILE`  | —         | Path to service account JSON key file  |
| `SMTP_HOST`                    | —         | SMTP server hostname (e.g. smtp.gmail.com) |
| `SMTP_PORT`                    | `587`     | SMTP server port                       |
| `SMTP_USERNAME`                | —         | SMTP login username                    |
| `SMTP_PASSWORD`                | —         | SMTP login password or App Password    |
| `SMTP_FROM_EMAIL`              | —         | Sender email address                   |
| `SMTP_FROM_NAME`               | —         | Sender display name                    |
| `RETELL_API_KEY`               | —         | RetellAI API key (future)              |

## Google Sheets Setup

The backend persists every successful booking to a Google Sheets spreadsheet.
If the credentials are not configured, the app starts normally and logs a
warning — bookings are still processed but not persisted.

### Step 1 — Create a Google Cloud Service Account

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Navigate to **APIs & Services → Library**.
4. Enable the **Google Sheets API** and the **Google Drive API**.
5. Navigate to **APIs & Services → Credentials**.
6. Click **Create Credentials → Service Account**.
7. Name it (e.g. `voice-receptionist-sheets`) and click **Done**.
8. Under the new service account, go to the **Keys** tab.
9. Click **Add Key → Create new key → JSON**.
10. Save the downloaded JSON file to your project (e.g. `backend/credentials.json`).

### Step 2 — Create & Share the Spreadsheet

1. Create a new Google Sheets spreadsheet.
2. Copy the spreadsheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/<THIS_IS_THE_ID>/edit
   ```
3. Share the spreadsheet with the service account email
   (found in the JSON key file as `client_email`) and give it **Editor** access.

### Step 3 — Configure Environment Variables

```bash
# In your .env file:
GOOGLE_SHEET_ID=your_spreadsheet_id_here
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
```

### Step 4 — Verify

Start the server. On the first booking request, the service will:

1. Authenticate using the service account.
2. Open the spreadsheet by ID.
3. Create an **Appointments** worksheet if it doesn't exist.
4. Insert the header row if it's missing.
5. Append the booking as a new row.

Check the logs for:
```
Google Sheets connected — spreadsheet=<ID> worksheet=Appointments
```

### Spreadsheet Columns

| Column             | Example                        |
|--------------------|--------------------------------|
| Booking ID         | BK-20260710-A1B2               |
| Name               | Rahul Sharma                   |
| Phone              | 9876543210                     |
| Email              | rahul@gmail.com                |
| Service            | Teeth Whitening                |
| Appointment Date   | 2026-07-10                     |
| Appointment Time   | 11:00                          |
| Booking Status     | Confirmed                      |
| Created At         | 2026-07-06T12:32:25+00:00      |

## Email Setup (SMTP)

The backend sends a booking confirmation email after a successful appointment booking is persisted to Google Sheets. 
If the SMTP credentials are not configured, the app operates in **disabled mode** — it logs a warning, skips email sending, and still processes the booking successfully.

### Step 1 — Generate a Gmail App Password (if using Gmail)

If you are using a standard Gmail account or Google Workspace, you cannot use your regular password. You must use an App Password:
1. Go to your [Google Account Manage page](https://myaccount.google.com/).
2. Navigate to **Security**.
3. Ensure **2-Step Verification** is turned on.
4. Go to **2-Step Verification** and scroll down to **App passwords**.
5. Create a new App Password (e.g., name it "Voice Receptionist").
6. Copy the 16-character password generated.

### Step 2 — Configure Environment Variables

```bash
# In your .env file:
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME="QuensultingAI Dental"
```

### Step 3 — Testing

Start the server. Submit a booking request with a valid `caller_email`.
The service will:
1. Validate the booking.
2. Persist the row to Google Sheets.
3. Authenticate with the SMTP server and send a plain-text confirmation email to the caller.
4. Return a successful booking API response.

Check the logs for:
```
Email service enabled — host=smtp.gmail.com port=587 from_email=your_email@gmail.com
...
Confirmation email sent successfully for booking BK-XXXXX-XXXX
```

## Architecture

The codebase follows **clean architecture** principles:

```
Router → Service → External Integration
  ↓         ↓              ↓
 HTTP    Business      Google Sheets
 layer    logic          API
```

- **`config/`** — Environment loading and validation.
- **`routes/`** — Thin HTTP layer. Each router handles a feature area.
- **`schemas/`** — Pydantic models for request/response serialization and validation.
- **`services/`** — Business logic, isolated from HTTP transport.
- **`models/`** — Domain entities, enums, and constants.
- **`utils/`** — Cross-cutting concerns (logging, validators).

## Phases

| Phase | Feature                                | Status |
|-------|----------------------------------------|--------|
| 1     | FastAPI foundation & health check      | ✅ Done |
| 2     | RetellAI conversation flow design      | ✅ Done |
| 3.1   | Webhook APIs for RetellAI              | ✅ Done |
| 3.2   | Google Sheets booking persistence      | ✅ Done |
| 3.3   | Email confirmations via SMTP           | ✅ Done |
| 5     | RetellAI agent integration             | Planned |

## License

Private — all rights reserved.

