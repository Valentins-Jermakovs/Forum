# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException

# Models:
from models.event import LibraryEvent



# =====================================================
#                Event Permission Validator
# =====================================================

# This class is responsible for validating permissions related to events. 
# It checks if a user has the necessary permissions to perform actions on an event, 
# such as modifying or deleting it.
class EventPermissionValidator:


    async def check_owner(
        self,
        event: LibraryEvent,
        user_id: int
    ) -> bool:

        # Check user permission to modify the event
        if event.creator_id != user_id:

            raise HTTPException(
                status_code=403,
                detail="You are not allowed to modify this event"
            )


        return True



# =====================================================
#              Event Uniqueness Validator
# =====================================================

# This class is responsible for validating the uniqueness 
# of event titles within a specific library.
class EventUniquenessValidator:


    async def check_title_unique(
        self,
        title: str,
        library: str,
        exclude_id: str | None = None
    ) -> None:


        query = {
            "title": title,
            "library": library
        }


        # Search existing event
        existing_event = await (
            LibraryEvent
            .find_one(query)
        )


        # Nothing found
        if not existing_event:
            return


        # During update ignore current event
        if exclude_id and str(existing_event.id) == exclude_id:
            return


        raise HTTPException(
            status_code=400,
            detail="Event with this title already exists in this library"
        )



# Create instance of the validator classes for use in other parts of the application.
event_permission_validator = EventPermissionValidator()
event_uniqueness_validator = EventUniquenessValidator()