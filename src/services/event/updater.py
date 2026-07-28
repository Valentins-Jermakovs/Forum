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
    event_uniqueness_validator,
    event_capacity_validator
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
        user_id: str,
        user_email: str,
        user_roles: list[str]
    ) -> LibraryEvent:


        try:

            # Normalize the event data
            data = event_normalizer.normalize_update(data)


            # New values
            new_title = data.title or event.title
            new_library = data.library or event.library


            # Check title uniqueness
            await event_uniqueness_validator.check_title_unique(
                title=new_title,
                library=new_library,
                exclude_id=str(event.id)
            )


            # Check owner permission
            await event_permission_validator.check_owner(
                event,
                user_id,
                user_roles
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


            # Validate new capacity
            await event_capacity_validator.check_capacity(
                event=event,
                new_capacity=update_data.get("capacity")
            )


            # Update fields
            for field, value in update_data.items():

                setattr(
                    event,
                    field,
                    value
                )


            # Update timestamp
            event.updated_at = datetime.now()


            # Save changes
            await event.save()


            # Success audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.UPDATE,
                entity=AuditEntity.EVENT,
                description="Updated library event",
                success=True,
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


        except Exception as error:


            # Failed audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.UPDATE,
                entity=AuditEntity.EVENT,
                description="Failed to update library event",
                success=False,
                metadata={
                    "event_id": str(event.id),
                    "title": event.title,
                    "error": str(error),
                    "error_type": type(error).__name__
                }
            )


            raise