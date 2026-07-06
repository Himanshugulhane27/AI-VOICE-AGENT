"""Route sub-package — API endpoint routers."""

from app.routes.appointments import router as appointments_router
from app.routes.clinic import router as clinic_router
from app.routes.faq import router as faq_router
from app.routes.health import router as health_router
from app.routes.transfer import router as transfer_router

__all__ = [
    "appointments_router",
    "clinic_router",
    "faq_router",
    "health_router",
    "transfer_router",
]
