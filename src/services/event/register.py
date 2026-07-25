# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException
from datetime import datetime

# Models:
from models import (
    LibraryEvent,
    Participant,
    EventStatus,
    AuditAction, 
    AuditEntity
)

# Schemas
from schemas.event import ParticipantCreate

# Services:
from services import audit_service



# =====================================================
#               Event Registration
# =====================================================

# This class is responsible for handling 
# the registration of participants to events.
class EventRegistration:

    async def register(
        self,
        event: LibraryEvent,
        participant: ParticipantCreate
    ) -> LibraryEvent:


        # Check event status
        if event.status != EventStatus.ACTIVE:

            raise HTTPException(
                status_code=400,
                detail="Event is not available"
            )


        # Check available seats
        if len(event.participants) >= event.capacity:

            raise HTTPException(
                status_code=400,
                detail="No available seats"
            )


        # Check duplicate registration
        for user in event.participants:

            if user.email == participant.email:

                raise HTTPException(
                    status_code=400,
                    detail="User already registered"
                )


        # Add participant
        event.participants.append(
            Participant(
                **participant.model_dump()
            )
        )


        # Update timestamp
        event.updated_at = datetime.now()


        # Save changes
        await event.save()

        # Write audit log
        await audit_service.create_log(
            user_email=participant.email,
            action=AuditAction.REGISTER,
            entity=AuditEntity.EVENT,
            description="Participant registered for event",
            metadata={
                "event_id": str(event.id),
                "event_title": event.title,
                "participant_name": participant.name
            }
        )


        return event