# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter

# Routes:
from .metrics import router as metrics_router
from .event import router as events_router
from .event_registrations import router as event_registrations_router
from .event_statistics import router as event_statistics_router
from .audit import router as audit_router



# =====================================================
#                       Router
# =====================================================

main_router = APIRouter()



# =====================================================
#         Connect app routes to the main router
# =====================================================

main_router.include_router(metrics_router)
main_router.include_router(events_router)
main_router.include_router(event_registrations_router)
main_router.include_router(event_statistics_router)
main_router.include_router(audit_router)