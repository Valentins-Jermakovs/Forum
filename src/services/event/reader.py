# =====================================================
#                        Imports
# =====================================================

# Models:
from models.event import LibraryEvent

# Query
from .query import EventQueryBuilder



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
        **filters
    ) -> dict:


        # Query the database for events based on the provided filters,
        query = self.query_builder.build(
            **filters
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
        return {
            "items": events,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": has_more
        }