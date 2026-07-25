# =====================================================
#                        Imports
# =====================================================

# Libraries:
from datetime import datetime

# Models:
from models import (
    LibraryEvent, 
    AuditAction, 
    AuditEntity
)

# Schemas:
from schemas.event import EventUpdate

# Classes:
from .validator import (
    event_permission_validator,
    event_uniqueness_validator
)
from .normalizer import event_normalizer

# Services:
from services import audit_service


# =====================================================
#                   Event Updater
# =====================================================

# This class is responsible for updating existing events.
class EventUpdater:

    async def update(
        self,
        event: LibraryEvent,
        data: EventUpdate,
        user_id: int,
        user_email: str
    ) -> LibraryEvent:

        # Normalize the event data (update)
        data = event_normalizer.normalize_update(data)


        # New values for title and library, 
        # if provided in the update data
        new_title = data.title or event.title
        new_library = data.library or event.library


        # Check if the new title is unique within the same library,
        # excluding the current event being updated
        await event_uniqueness_validator.check_title_unique(
            title=new_title,
            library=new_library,
            exclude_id=str(event.id)
        )


        # Check owner
        await event_permission_validator.check_owner(
            event,
            user_id
        )

        # Save old values for audit
        old_data = {
            "title": event.title,
            "library": event.library,
            "place": event.place,
            "category": event.category.value,
            "status": event.status.value
        }


        # Get only provided fields
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

        # Write audit log
        await audit_service.create_log(
            user_email=user_email,
            action=AuditAction.UPDATE,
            entity=AuditEntity.EVENT,
            description="Updated library event",
            metadata={
                "event_id": str(event.id),
                "changed_fields": list(
                    update_data.keys()
                ),
                "old_data": old_data,
                "new_data": update_data
            }
        )

        return event