# =====================================================
#                        Imports
# =====================================================

# Models:
from models.event import (
    LibraryEvent, 
    EventCategory, 
    EventStatus
)

# Query
from .query import EventQueryBuilder

# Schemas:
from schemas import EventsResponse



# =====================================================
#                   Event Reader
# =====================================================

# This class is responsible for reading events from the database.
class EventReader:

    # Constructor - initializes the EventQueryBuilder 
    # to build query dictionaries based on provided filters.
    def __init__(self):

        self.query_builder = EventQueryBuilder()



    async def get_events(
        self,
        offset: int = 0,
        limit: int = 20,
        title: str | None = None,
        library: str | None = None,
        category: EventCategory | None = None,
        status: EventStatus | None = None,
        creator_id: int | None = None,
        event_date: str | None = None,
        participant_email: str | None = None
    ) -> EventsResponse:


        # Query the database for events based on the provided filters,
        query = self.query_builder.build(
            title=title,
            library=library,
            category=category,
            status=status,
            creator_id=creator_id,
            event_date=event_date,
            participant_email=participant_email
        )

        # List of events and total count of events matching the query
        events = await (
            LibraryEvent
            .find(query)
            .sort(
                -LibraryEvent.created_at
            )
            .skip(offset)
            .limit(limit)
            .to_list()
        )


        # Count total number of events matching the query
        total = await (
            LibraryEvent
            .find(query)
            .count()
        )

        # Check if there are more events to fetch based on the offset and limit
        has_more = offset + limit < total

        # Return a dictionary containing the list of 
        # events, total count, offset, limit, and a 
        # boolean indicating if there are more events to fetch.
        return EventsResponse(
            items=events,
            total=total,
            offset=offset,
            limit=limit,
            has_more=has_more
        )