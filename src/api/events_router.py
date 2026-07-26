# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter, Depends

# Schemas
from schemas import (
    EventCategory,
    EventStatus,
    EventCreate,
    EventUpdate,
    EventResponse,
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
    data: EventCreate,
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
        data=data,
        user_id=user_id,
        user_email=user_email
    )

    return created_event


# Endpoint for updating an event
@router.put(
    "/update/{event_id}",
    response_model=EventResponse,
    summary="Update an existing event"
)
async def update_event(
    event_id: str,
    data: EventUpdate,
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

    # Find event by id
    event = await event_service.find_by_id(
        event_id
    )


    # Update the event using the service
    updated_event = await event_service.update(
        event=event,
        data=data,
        user_id=user_id,
        user_email=user_email
    )

    return updated_event


# Endpoint for deleting an event
@router.delete(
    "/delete/{event_id}",
    response_model=dict,
    summary="Delete an existing event"
)
async def delete_event(
    event_id: str,
    payload = Depends(jwt_validator.validate_token),
) -> dict:

    # Admin role check
    await jwt_validator.require_roles(
        roles=["admin", "librarian"],
        payload=payload
    )

    # Get user_id and user_email
    user_id = jwt_payload.get_user_id(payload)
    user_email = jwt_payload.get_user_email(payload)

    # Find event by id
    event = await event_service.find_by_id(
        event_id
    )


    # Delete the event using the service
    deleted_event_response = await event_service.delete(
        event=event,
        user_id=user_id,
        user_email=user_email
    )

    return deleted_event_response


# Endpoint for searching events with optional filters
@router.get(
    "/search",
    response_model=EventsResponse,
    summary="Search for events with optional filters"
)
async def search_events(
    offset: int = 0,
    limit: int = 20,
    title: str | None = None,
    library: str | None = None,
    category: EventCategory | None = None,
    status: EventStatus | None = None,
    creator_id: int | None = None,
    event_date: str | None = None,
    participant_email: str | None = None,
    payload = Depends(jwt_validator.validate_token)
) -> EventsResponse:
    
    # Search for events using the service
    events_response = await event_service.get(
        offset=offset,
        limit=limit,
        title=title,
        library=library,
        category=category,
        status=status,
        creator_id=creator_id,
        event_date=event_date,
        participant_email=participant_email
    )

    return events_response


# Endpoint for finding an event by its ID
@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get an event by its ID"
)
async def get_event_by_id(
    event_id: str,
    payload = Depends(jwt_validator.validate_token)
) -> EventResponse:
    
    # Find event by id
    event = await event_service.find_by_id(
        event_id
    )

    return event


