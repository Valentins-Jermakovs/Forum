# =====================================================
#                        Imports
# =====================================================

from fastapi import HTTPException

from models import LibraryEvent

from repositories import event_repository



# =====================================================
#                   Event Finder
# =====================================================


class EventFinder:


    async def get_by_id(
        self,
        event_id: str
    ) -> LibraryEvent:


        event = await event_repository.find_by_id(
            event_id
        )


        if not event:

            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )


        return event