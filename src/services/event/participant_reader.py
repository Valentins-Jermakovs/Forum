# =====================================================
#                        Imports
# =====================================================

# Models:
from models import LibraryEvent

# Repository:
from repositories import event_repository

# Classes:
from utils import event_query_builder

# Schemas:
from schemas import (
    EventsResponse,
    EventResponse,
    ParticipantResponse
)



# =====================================================
#              Participant Event Reader
# =====================================================

# This class is responsible for reading events
# that a participant has registered for.
#
# It does not communicate directly with MongoDB.
# All database operations are handled by EventRepository.
class ParticipantEventReader:


    async def get_registered_events(
        self,
        email: str,
        offset: int = 0,
        limit: int = 20
    ) -> EventsResponse:


        # Build query
        query = event_query_builder.build(
            participant_email=email
        )


        # Get events from repository
        events, total = await event_repository.search(
            query=query,
            offset=offset,
            limit=limit,
            sort=-LibraryEvent.event_date
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