# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException
import datetime

# Models:
from models.event import LibraryEvent



# =====================================================
#          Event Cancellation Service
# =====================================================

# This class is responsible for handling 
# the cancellation of participant registrations for events.
class EventCancellationService:

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


        return event