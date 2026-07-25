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


# =====================================================
#                   Event Cancellation
# =====================================================

# This class is responsible for handling 
# the cancellation of participant registrations for events.
class EventCancellation:

    async def cancel(
        self,
        event: LibraryEvent,
        email: str
    ) -> LibraryEvent:


        participant = None


        # Find participant
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



        # Remove participant
        event.participants.remove(
            participant
        )


        # Update timestamp
        event.updated_at = datetime.now()


        # Save
        await event.save()

        # Write audit log
        await audit_service.create_log(
            user_email=participant.email,
            action=AuditAction.CANCEL_REGISTRATION,
            entity=AuditEntity.EVENT,
            description="Cancelled participant registration",
            metadata={
                "event_id": str(event.id),
                "event_title": event.title,
                "participant_name": participant.name
            }
        )

        return event