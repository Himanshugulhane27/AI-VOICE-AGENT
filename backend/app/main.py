"""AI Voice Receptionist — application entry point.

Creates, configures, and exposes the FastAPI application instance.
Run with::

    uvicorn app.main:app --reload
"""

import logging
import time
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import get_settings
from app.routes import (
    appointments_router,
    clinic_router,
    faq_router,
    health_router,
    transfer_router,
)
from app.utils import request_id_ctx, setup_logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler — runs on startup and shutdown."""
    try:
        settings = get_settings()
    except ValidationError as exc:
        print(f"Configuration validation failed: {exc}")
        raise RuntimeError("Invalid configuration") from exc

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

    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Catch all unhandled exceptions."""
        req_id = request_id_ctx.get("")
        logger.exception("Unhandled server error — %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "request_id": req_id,
            },
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Return validation errors in a consistent JSON shape."""
        req_id = request_id_ctx.get("")
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
                "request_id": req_id,
            },
        )

    # -- Middleware: request logging -----------------------------------------

    @application.middleware("http")
    async def request_middleware(request: Request, call_next) -> Response:  # type: ignore[type-arg]
        """Log incoming requests, inject request IDs, and measure duration."""
        req_id = str(uuid.uuid4())
        request_id_ctx.set(req_id)
        
        start_time = time.perf_counter()
        
        response: Response = await call_next(request)
        
        duration = round((time.perf_counter() - start_time) * 1000, 2)
        
        logger.info(
            "Request processed — route=%s method=%s status=%s duration=%sms",
            request.url.path,
            request.method,
            response.status_code,
            duration,
        )
        
        response.headers["X-Request-ID"] = req_id
        return response

    # -- Routers -------------------------------------------------------------
    application.include_router(health_router)
    application.include_router(appointments_router)
    application.include_router(faq_router)
    application.include_router(transfer_router)
    application.include_router(clinic_router)

    return application


app = create_app()

