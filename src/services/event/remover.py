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
from .validator import event_permission_validator

# Services:
from services import audit_service



# =====================================================
#                   Event Remover
# =====================================================

# This class is responsible for removing events from the database.
class EventRemover:


    async def delete(
        self,
        event: LibraryEvent,
        user_id: int,
        user_email: str,
        user_roles: list[str]
    ):


        try:

            # Check if the user is the owner of the event
            await event_permission_validator.check_owner(
                event,
                user_id,
                user_roles
            )


            # Save event information before deletion
            event_data = {
                "event_id": str(event.id),
                "title": event.title,
                "library": event.library,
                "category": event.category.value,
                "status": event.status.value
            }


            # Delete event from database
            await event.delete()


            # Success audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.DELETE,
                entity=AuditEntity.EVENT,
                description="Deleted library event",
                success=True,
                metadata=event_data
            )


            return {
                "message": "Event deleted successfully",
                "event_id": str(event.id)
            }


        except Exception as error:


            # Failed audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.DELETE,
                entity=AuditEntity.EVENT,
                description="Failed to delete library event",
                success=False,
                metadata={
                    "event_id": str(event.id),
                    "title": event.title,
                    "error": str(error),
                    "error_type": type(error).__name__
                }
            )


            raise