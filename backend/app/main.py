"""AI Voice Receptionist — application entry point.

Creates, configures, and exposes the FastAPI application instance.
Run with::

    uvicorn app.main:app --reload
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routes import (
    appointments_router,
    clinic_router,
    faq_router,
    health_router,
    transfer_router,
)
from app.utils import setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — runs on startup and shutdown."""
    settings = get_settings()
    setup_logging(level=settings.log_level)
    logger.info(
        "Server starting — host=%s port=%s log_level=%s",
        settings.host,
        settings.port,
        settings.log_level,
    )
    yield
    logger.info("Server shutting down")


def create_app() -> FastAPI:
    """Construct and return the configured FastAPI application."""
    application = FastAPI(
        title="AI Voice Receptionist",
        description=(
            "Production-ready backend for the QuensultingAI Dental Clinic "
            "AI-powered voice receptionist. Provides webhook endpoints "
            "consumed by RetellAI Function Nodes."
        ),
        version="0.2.0",
        lifespan=lifespan,
    )

    # -- Exception handlers --------------------------------------------------

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Return validation errors in a consistent JSON shape.

        Maps Pydantic validation errors into the ``BaseResponse``
        envelope so RetellAI always receives ``success`` and ``message``
        fields, even on bad input.
        """
        errors = []
        for error in exc.errors():
            field = " → ".join(str(loc) for loc in error["loc"])
            errors.append(f"{field}: {error['msg']}")

        detail = "; ".join(errors)
        logger.warning("Validation error — %s %s — %s", request.method, request.url.path, detail)

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": f"Validation failed: {detail}",
            },
        )

    # -- Middleware: request logging -----------------------------------------

    @application.middleware("http")
    async def log_requests(request: Request, call_next) -> Response:  # type: ignore[type-arg]
        """Log every incoming HTTP request."""
        logger.info("Incoming request — %s %s", request.method, request.url.path)
        response: Response = await call_next(request)
        logger.info(
            "Response — %s %s status=%s",
            request.method,
            request.url.path,
            response.status_code,
        )
        return response

    # -- Routers -------------------------------------------------------------
    application.include_router(health_router)
    application.include_router(appointments_router)
    application.include_router(faq_router)
    application.include_router(transfer_router)
    application.include_router(clinic_router)

    return application


app = create_app()

