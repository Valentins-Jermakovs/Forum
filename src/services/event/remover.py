# =====================================================
#                        Imports
# =====================================================

# Models:
from models import (
    LibraryEvent, 
    AuditAction, 
    AuditEntity
)

# Classes:
from .validator import EventPermissionValidator

# Services:
from services import audit_service



# =====================================================
#                   Event Remover
# =====================================================

# This class is responsible for removing events from the database.
class EventRemover:

    # Constructor - initializes the EventPermissionValidator 
    # to check user permissions before deleting an event.
    def __init__(
        self
    ):

        self.permission = EventPermissionValidator()



    async def delete(
        self,
        event: LibraryEvent,
        user_id: int,
        user_email: str
    ):

        # Check if the user is the owner of the event
        await self.permission.check_owner(
            event,
            user_id
        )

        # Save event information before deletion
        event_data = {
            "event_id": str(event.id),
            "title": event.title,
            "library": event.library,
            "category": event.category.value,
            "status": event.status.value
        }

        # Delete event from data base
        await event.delete()

        # Write audit log
        await audit_service.create_log(
            user_email=user_email,
            action=AuditAction.DELETE,
            entity=AuditEntity.EVENT,
            description="Deleted library event",
            metadata=event_data
        )

        return {
            "message": "Event deleted successfully",
            "event_id": str(event.id)
        }