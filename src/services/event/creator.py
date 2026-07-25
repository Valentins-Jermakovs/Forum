# =====================================================
#                        Imports
# =====================================================

# Models:
from models.event import LibraryEvent

# Schemas:
from schemas.event import EventCreate



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


        # Create a new LibraryEvent instance with the provided data, 
        # user ID, and email.
        event = LibraryEvent(
            **data.model_dump(),

            creator_id=user_id,

            created_by=user_email
        )

        # Save the new event to the database
        await event.insert()


        return event