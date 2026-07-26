# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter

# Routes:
from .metrics_router import router as metrics_router



# Main router object
main_router = APIRouter()



# =====================================================
#         Connect app routes to the main router
# =====================================================

main_router.include_router(metrics_router)