# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import (
    APIRouter, 
    Depends
)

# Schemas
from schemas import (
    UpcomingEventsResponse,
    PopularEventsResponse
)

# Utils
from utils import jwt_validator

# Services
from services import event_service



# =====================================================
#                       Router
# =====================================================

router = APIRouter(
    prefix="/events/statistics",
    tags=["Event Statistics"]
)



# =====================================================
#                       Endpoints
# =====================================================

# Endpoint for getting upcoming event list
@router.get(
    "/upcoming",
    response_model=UpcomingEventsResponse,
    summary="Get upcoming events"
)
async def get_upcoming_events(
    limit: int = 10,
    payload = Depends(jwt_validator.validate_token)
):

    return await event_service.get_upcoming_events(
        limit=limit
    )


# Event for getting most popular event list
# based on participiants number
@router.get(
    "/popular",
    response_model=PopularEventsResponse,
    summary="Get popular events"
)
async def get_popular_events(
    limit: int = 10,
    payload = Depends(jwt_validator.validate_token)
):
    
    return await event_service.get_popular_events(
        limit=limit
    )