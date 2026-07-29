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


# Repositories:
from repositories import event_repository


# Classes:
from utils import event_normalizer
from .validator import event_uniqueness_validator



# =====================================================
#                   Event Creator
# =====================================================

# This class is responsible for creating new events.
#
# Responsibilities:
# - normalize event data
# - validate event uniqueness
# - create event object
# - save event through repository
# - write audit logs
#
# Database operations are delegated to repository.
class EventCreator:



    async def create(
        self,
        data: EventCreate,
        user_id: str,
        user_email: str
    ) -> LibraryEvent:


        try:

            # Normalize event data
            data = event_normalizer.normalize_create(
                data
            )



            # Validate event title uniqueness
            await event_uniqueness_validator.check_title_unique(
                title=data.title,
                library=data.library
            )



            # Create event document
            event = LibraryEvent(
                **data.model_dump(),
                creator_id=user_id,
                created_by=user_email
            )



            # Save event through repository
            await event_repository.create(
                event
            )



            # Successful audit log
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


            # Failed audit log
            await audit_service.create_log(
                user_email=user_email,
                action=AuditAction.CREATE,
                entity=AuditEntity.EVENT,
                description="Failed to create library event",
                success=False,
                metadata={
                    "title": data.title,
                    "library": data.library,
                    "error": str(error),
                    "error_type": type(error).__name__
                }
            )


            # Re-raise original exception
            raise