# =====================================================
#                        Imports
# =====================================================

# Models:
from models import LibraryEvent
from models.event import (
    EventCategory,
    EventStatus
)

# Repository:
from repositories import event_repository

# Query:
from utils import event_query_builder

# Schemas:
from schemas import (
    EventsResponse,
    EventResponse,
    ParticipantResponse
)



# =====================================================
#                   Event Reader
# =====================================================

# This class is responsible for reading events.
#
# Database operations are delegated to EventRepository.
# This class only handles query building and response mapping.
class EventReader:


    async def get_events(
        self,
        offset: int = 0,
        limit: int = 20,
        title: str | None = None,
        library: str | None = None,
        category: EventCategory | None = None,
        status: EventStatus | None = None,
        creator_email: str | None = None,
        event_date: str | None = None,
        participant_email: str | None = None
    ) -> EventsResponse:


        # Build query
        query = event_query_builder.build(
            title=title,
            library=library,
            category=category,
            status=status,
            creator_email=creator_email,
            event_date=event_date,
            participant_email=participant_email
        )


        # Get events from repository
        events, total = await event_repository.search(
            query=query,
            offset=offset,
            limit=limit,
            sort=-LibraryEvent.created_at
        )


        # Pagination check
        has_more = offset + limit < total



        return EventsResponse(
            items=[
                EventResponse(
                    id=str(event.id),
                    title=event.title,
                    description=event.description,
                    library=event.library,
                    place=event.place,
                    tags=event.tags,
                    event_date=event.event_date,
                    event_time=event.event_time,
                    duration=event.duration,
                    capacity=event.capacity,
                    participants=[
                        ParticipantResponse(
                            name=participant.name,
                            email=participant.email,
                            phone=participant.phone
                        )
                        for participant in event.participants
                    ],
                    category=event.category,
                    status=event.status,
                    created_by=event.created_by,
                    created_at=event.created_at,
                    updated_at=event.updated_at
                )
                for event in events
            ],
            total=total,
            offset=offset,
            limit=limit,
            has_more=has_more
        )