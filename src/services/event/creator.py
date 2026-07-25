# =====================================================
#                        Imports
# =====================================================

# Models:
from models import (
    LibraryEvent, 
    AuditAction, 
    AuditEntity
)

# Schemas:
from schemas.event import EventCreate

# Services:
from services import audit_service

# Classes
from .normalizer import event_normalizer
from .validator import event_uniqueness_validator


# =====================================================
#                   Event Creator
# =====================================================

# This class is responsible for creating new events. 
# It takes the event data, along with the user ID and email of the creator, 
# and creates a new LibraryEvent instance in the database.
class EventCreator:

    async def create(
        self,
        data: EventCreate,
        user_id: int,
        user_email: str
    ) -> LibraryEvent:

        try:

            # Normalize data
            data = event_normalizer.normalize_create(data)


            # Validate uniqueness
            await event_uniqueness_validator.check_title_unique(
                title=data.title,
                library=data.library
            )


            # Create event
            event = LibraryEvent(
                **data.model_dump(),
                creator_id=user_id,
                created_by=user_email
            )


            # Save event
            await event.insert()


            # Success audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.CREATE,
                entity=AuditEntity.EVENT,
                description="Created library event",
                success=True,
                metadata={
                    "event_id": str(event.id),
                    "title": event.title
                }
            )


            return event


        except Exception as error:


            # Failed audit
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.CREATE,
                entity=AuditEntity.EVENT,
                description="Failed to create library event",
                success=False,
                metadata={
                    "title": data.title,
                    "library": data.library,
                    "error": str(error)
                }
            )


            # Return original error
            raise