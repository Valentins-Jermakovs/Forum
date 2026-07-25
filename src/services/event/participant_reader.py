# =====================================================
#                        Imports
# =====================================================

# Models:
from models.event import LibraryEvent

# Classes:
from .query import EventQueryBuilder



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
    ) -> dict:

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

        return {
            "items": events,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": has_more
        }