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

        # Normalize the event data
        data = event_normalizer.normalize_create(data)

        # Validate event uniqueness
        await event_uniqueness_validator.check_title_unique(
            title=data.title,
            library=data.library
        )

        # Create a new LibraryEvent instance with the provided data, 
        # user ID, and email.
        event = LibraryEvent(
            **data.model_dump(),
            creator_id=user_id,
            created_by=user_email
        )

        # Save the new event to the database
        await event.insert()

        # Write audit log
        await audit_service.create_log(
            user_email=user_email,
            action=AuditAction.CREATE,
            entity=AuditEntity.EVENT,
            description="Created library event",
            metadata={
                "event_id": str(event.id),
                "title": event.title
            }
        )


        return event