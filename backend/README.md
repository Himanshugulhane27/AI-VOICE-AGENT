# AI Voice Receptionist — Backend

Production-ready FastAPI backend foundation for an AI-powered voice receptionist.

## Project Structure

```
backend/
├── main.py                  # CLI entry point (python main.py)
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .env                     # Local environment overrides (git-ignored)
└── app/
    ├── __init__.py
    ├── main.py              # FastAPI application factory
    ├── config/
    │   ├── __init__.py
    │   └── settings.py      # Pydantic Settings (typed env loading)
    ├── routes/
    │   ├── __init__.py
    │   └── health.py        # GET /health endpoint
    ├── services/
    │   └── __init__.py      # Business-logic layer (future)
    ├── models/
    │   └── __init__.py      # Domain / DB models (future)
    ├── schemas/
    │   ├── __init__.py
    │   └── health.py        # Pydantic response schemas
    └── utils/
        ├── __init__.py
        └── logging.py       # Structured logging configuration
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
# Edit .env if you need to change HOST, PORT, or LOG_LEVEL
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

| Method | Path      | Description         |
|--------|-----------|---------------------|
| GET    | `/health` | Service health check |

## Configuration

All configuration is loaded from environment variables (or a `.env` file) via **pydantic-settings**.

| Variable         | Default     | Description                     |
|------------------|-------------|---------------------------------|
| `HOST`           | `0.0.0.0`   | Server bind address             |
| `PORT`           | `8000`      | Server bind port                |
| `LOG_LEVEL`      | `info`      | Logging verbosity               |
| `GOOGLE_SHEET_ID`| —           | Google Sheets ID (future)       |
| `SMTP_EMAIL`     | —           | Sender email address (future)   |
| `SMTP_PASSWORD`  | —           | SMTP password (future)          |
| `RETELL_API_KEY` | —           | RetellAI API key (future)       |

## Architecture

The codebase follows **clean architecture** principles:

- **`config/`** — Environment loading and validation. Single source of truth for settings.
- **`routes/`** — Thin HTTP layer. Each router handles a feature area.
- **`schemas/`** — Pydantic models for request/response serialization and validation.
- **`services/`** — Business logic, isolated from HTTP transport.
- **`models/`** — Domain entities and persistence models.
- **`utils/`** — Cross-cutting concerns (logging, helpers).

## Future Phases

| Phase | Feature                         |
|-------|---------------------------------|
| 2     | RetellAI voice agent webhook    |
| 3     | Google Sheets appointment log   |
| 4     | Email confirmations via SMTP    |
| 5     | Appointment booking logic       |

## License

Private — all rights reserved.
