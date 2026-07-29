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

# Schemas:
from schemas.event import ParticipantCreate

# Repository:
from repositories import event_repository

# Services:
from services import audit_service

# Classes:
from utils import event_normalizer



# =====================================================
#               Event Registration
# =====================================================

# This class is responsible for handling 
# the registration of participants to events.
#
# Database operations are delegated to EventRepository.
# This class only handles business logic.
class EventRegistration:


    async def register(
        self,
        event: LibraryEvent,
        participant: ParticipantCreate,
        email: str
    ) -> LibraryEvent:


        try:

            # Normalize participant data
            participant = event_normalizer.normalize_participant(
                participant
            )


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

                if user.email == email:

                    raise HTTPException(
                        status_code=400,
                        detail="User already registered"
                    )


            # Add participant
            event.participants.append(
                Participant(
                    name=participant.name,
                    phone=participant.phone,
                    email=email
                )
            )


            # Update timestamp
            event.updated_at = datetime.now()


            # Save changes through repository
            await event_repository.save(
                event
            )


            # Success audit
            await audit_service.create_log(
                user_email=email,
                action=AuditAction.REGISTER,
                entity=AuditEntity.EVENT,
                description="Participant registered for event",
                success=True,
                metadata={
                    "event_id": str(event.id),
                    "event_title": event.title,
                    "participant_name": participant.name
                }
            )


            return event


        except Exception as error:


            # Failed audit
            await audit_service.create_log(
                user_email=email,
                action=AuditAction.REGISTER,
                entity=AuditEntity.EVENT,
                description="Failed to register participant for event",
                success=False,
                metadata={
                    "event_id": str(event.id),
                    "event_title": event.title,
                    "participant_name": participant.name,
                    "error": str(error),
                    "error_type": type(error).__name__
                }
            )


            raise