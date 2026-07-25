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