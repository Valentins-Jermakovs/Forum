# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException

# Models
from models.event import LibraryEvent



# =====================================================
#                   Event Finder
# =====================================================

# This class is responsible for finding
# a single event by its ID.
class EventFinder:


    async def get_by_id(
        self,
        event_id: str
    ) -> LibraryEvent:

        # Get event by ID
        event = await LibraryEvent.get(
            event_id
        )


        # If the event is not found, raise a 404 HTTPException
        if not event:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )


        return event