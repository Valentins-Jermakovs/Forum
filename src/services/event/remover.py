# =====================================================
#                        Imports
# =====================================================

# Models
from models.event import LibraryEvent

# Classes:
from .validator import EventPermissionValidator



# =====================================================
#                   Event Remover
# =====================================================

# This class is responsible for removing events from the database.
class EventRemover:

    # Constructor - initializes the EventPermissionValidator 
    # to check user permissions before deleting an event.
    def __init__(self):

        self.permission = EventPermissionValidator()



    async def delete(
        self,
        event: LibraryEvent,
        user_id: int
    ):

        # Check if the user is the owner of the event
        await self.permission.check_owner(
            event,
            user_id
        )

        # Delete event from data base
        await event.delete()