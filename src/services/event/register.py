# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException
import datetime

# Models:
from models.event import (
    LibraryEvent,
    Participant,
    EventStatus
)

# Schemas
from schemas.event import ParticipantCreate



# =====================================================
#              Event Registration Service
# =====================================================

# This class is responsible for handling 
# the registration of participants to events.
class EventRegistrationService:


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


        return event