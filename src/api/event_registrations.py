# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter, Depends

# Schemas
from schemas import (
    EventResponse,
    ParticipantCreate,
    EventCategory,
    EventStatus,
    EventCreate,
    EventUpdate,
    EventsResponse
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
    prefix="/events/{event_id}/registrations",
    tags=["Event Registrations services - response of users registrations to events"],
)



# =====================================================
#                       Endpoints
# =====================================================

# Endpoint for registering a user to an event
@router.post(
    "",
    response_model=EventResponse,
    summary="Register a user to an event"
)
async def register_user_to_event(
    event_id: str,
    data: ParticipantCreate,
    payload = Depends(jwt_validator.validate_token),
) -> EventResponse:


    # Find event by id
    event = await event_service.find_by_id(
        event_id
    )

    # Register the participant to the event
    registered_event = await event_service.register(
        event=event,
        participant=data
    )

    return registered_event


# Endpoint for canceling a user's registration to an event
@router.delete(
    "",
    response_model=EventResponse,
    summary="Cancel a user's registration to an event"
)
async def cancel_user_registration_to_event(
    event_id: str,
    payload = Depends(jwt_validator.validate_token),
) -> EventResponse:

    # Find event by id
    event = await event_service.find_by_id(
        event_id
    )

    # Get user email from JWT payload
    email = jwt_payload.get_user_email(
        payload
    )

    # Cancel the participant's registration to the event
    canceled_event = await event_service.cancel_registration(
        event=event,
        email=email
    )

    return canceled_event


# Endpoint for getting user events, where user is registered as a participant
@router.get(
    "",
    response_model=EventsResponse,
    summary="Get user events where user is registered as a participant"
)
async def get_user_registered_events(
    offset: int = 0,
    limit: int = 20,
    payload = Depends(jwt_validator.validate_token),
) -> EventsResponse:

    # Get user email from JWT payload
    email = jwt_payload.get_user_email(
        payload
    )

    # Get events where the user is registered as a participant
    user_events = await event_service.get_user_events(
        offset=offset,
        limit=limit,
        email=email
    )

    return user_events
