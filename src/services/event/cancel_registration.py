# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException
from datetime import datetime


# Models:
from models import (
    LibraryEvent,
    AuditAction,
    AuditEntity
)


# Services:
from services import audit_service


# Repositories:
from repositories import event_repository



# =====================================================
#                   Event Cancellation
# =====================================================

# This class is responsible for handling
# the cancellation of participant registrations for events.
#
# Responsibilities:
# - find participant registration
# - remove participant
# - update event timestamp
# - save changes through repository
# - write audit logs
#
# Database operations are delegated to repository.
class EventCancellation:



    async def cancel(
        self,
        event: LibraryEvent,
        email: str
    ) -> LibraryEvent:


        # Store participant
        participant = None



        try:

            # Find participant by email
            for user in event.participants:

                if user.email == email:

                    participant = user
                    break



            # Participant not found
            if not participant:

                raise HTTPException(
                    status_code=404,
                    detail="Registration not found"
                )



            # Remove participant from event
            event.participants.remove(
                participant
            )



            # Update modification timestamp
            event.updated_at = datetime.now()



            # Save changes through repository
            await event_repository.save(
                event
            )



            # Successful audit log
            await audit_service.create_log(
                user_email=participant.email,
                action=AuditAction.CANCEL_REGISTRATION,
                entity=AuditEntity.EVENT,
                description="Cancelled participant registration",
                success=True,
                metadata={
                    "event_id": str(event.id),
                    "event_title": event.title,
                    "participant_name": participant.name
                }
            )



            return event



        except Exception as error:


            # Failed audit log
            await audit_service.create_log(
                user_email=email,
                action=AuditAction.CANCEL_REGISTRATION,
                entity=AuditEntity.EVENT,
                description="Failed to cancel participant registration",
                success=False,
                metadata={
                    "event_id": str(event.id),
                    "event_title": event.title,
                    "participant_email": email,
                    "error": str(error),
                    "error_type": type(error).__name__
                }
            )


            raise