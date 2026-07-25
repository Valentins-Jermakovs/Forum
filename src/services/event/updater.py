# =====================================================
#                        Imports
# =====================================================

# Libraries:
import datetime

# Models:
from models.event import LibraryEvent

# Schemas:
from schemas.event import EventUpdate

# Classes:
from .validator import EventPermissionValidator



# =====================================================
#                   Event Updater
# =====================================================

# This class is responsible for updating existing events.
class EventUpdater:

    # Constructor - initializes the EventPermissionValidator 
    # to check user permissions before updating an event.
    def __init__(self):

        self.permission = EventPermissionValidator()



    async def update(
        self,
        event: LibraryEvent,
        data: EventUpdate,
        user_id: int
    ) -> LibraryEvent:


        # Check owner
        await self.permission.check_owner(
            event,
            user_id
        )


        # Update event fields with the provided data, 
        # excluding any fields that are None.
        update_data = data.model_dump(
            exclude_none=True
        )


        # Set the new values for the event fields
        for field, value in update_data.items():

            setattr(
                event,
                field,
                value
            )

        # Update the updated_at timestamp to the current time
        event.updated_at = datetime.now()

        # Update the event in the database
        await event.save()


        return event