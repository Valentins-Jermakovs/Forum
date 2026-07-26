# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter, Depends

# Schemas
from schemas import (
    EventCategory,
    EventStatus,
    ParticipantCreate,
    ParticipantResponse,
    EventCreate,
    EventUpdate,
    RegisterParticipantRequest,
    EventResponse,
    EventsResponse,
    EventStatisticsResponse,
    UpcomingEventsResponse,
    PopularEventsResponse
)

# Utils
from utils import (
    jwt_validator, 
    jwt_payload
)

# Services
from services import event_service



# Router object
router = APIRouter(
    prefix="/events",
    tags=["Events services - create, read, update, delete events"],
)



# =====================================================
#                       Endpoints
# =====================================================

# Endpoint for creating an event
@router.post(
    "/create",
    response_model=EventResponse,
    summary="Create a new event"
)
async def create_event(
    event: EventCreate,
    payload = Depends(jwt_validator.validate_token),
) -> EventResponse:

    # Admin role check
    await jwt_validator.require_roles(
        roles=["admin", "librarian"],
        payload=payload
    )

    # Get user_id and user_email
    user_id = jwt_payload.get_user_id(payload)
    user_email = jwt_payload.get_user_email(payload)

    # Create the event using the service
    created_event = await event_service.create(
        data=event,
        user_id=user_id,
        user_email=user_email
    )

    return created_event