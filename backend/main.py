"""CLI entry point for running the server directly.

Usage::

    python -m backend.main
    # or simply:
    python main.py

Prefer ``uvicorn app.main:app --reload`` during development.
"""

import uvicorn

from app.config import get_settings


def main() -> None:
    """Start the uvicorn server with settings from the environment."""
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
    )


if __name__ == "__main__":
    main()
