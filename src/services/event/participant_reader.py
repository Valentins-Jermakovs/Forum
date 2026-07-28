# =====================================================
#                        Imports
# =====================================================

# Models:
from models.event import LibraryEvent

# Classes:
from .query import EventQueryBuilder

# Schemas:
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
class ParticipantEventReader:

    # Constructor - initializes the EventQueryBuilder
    # for building queries to fetch participant events.
    def __init__(self):

        self.query_builder = EventQueryBuilder()



    async def get_registered_events(
        self,
        email: str,
        offset: int = 0,
        limit: int = 20
    ) -> EventsResponse:

        # Query
        query = self.query_builder.build(
            participant_email=email
        )

        # List of events
        events = await (
            LibraryEvent
            .find(query)
            .sort(
                -LibraryEvent.event_date
            )
            .skip(offset)
            .limit(limit)
            .to_list()
        )

        # Count total events for pagination
        total = await (
            LibraryEvent
            .find(query)
            .count()
        )

        # Check if there are more events to fetch
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