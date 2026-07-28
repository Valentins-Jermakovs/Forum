# =====================================================
#                   Event Query Builder
# =====================================================

# Models:
from models.event import (
    EventCategory,
    EventStatus
)

# Utils:
from utils import (
    string_normalizer,
    email_normalizer,
    date_normalizer
)



# =====================================================
#                Event Query Builder
# =====================================================

# This class is responsible for building a query dictionary 
# based on the provided parameters.
class EventQueryBuilder:


    def build(
        self,
        title: str | None = None,
        library: str | None = None,
        category: EventCategory | None = None,
        status: EventStatus | None = None,
        creator_email: str | None = None,
        event_date: str | None = None,
        participant_email: str | None = None
    ) -> dict:


        # Query
        query = {}



        # --------------------------------------
        #              Normalization
        # --------------------------------------

        # Normalize title
        if title:

            title = string_normalizer.normalize(
                title
            )


        # Normalize library
        if library:

            library = string_normalizer.normalize(
                library
            )


        # Normalize creator email
        if creator_email:

            creator_email = email_normalizer.normalize(
                creator_email
            )


        # Normalize participant email
        if participant_email:

            participant_email = email_normalizer.normalize(
                participant_email
            )


        # Normalize event date
        if event_date:

            event_date = date_normalizer.normalize(
                event_date
            )



        # --------------------------------------
        #               Filters
        # --------------------------------------

        # Title
        if title:

            query["title"] = {
                "$regex": title,
                "$options": "i"
            }


        # Library
        if library:

            query["library"] = {
                "$regex": library,
                "$options": "i"
            }


        # Category
        if category:

            query["category"] = category


        # Status
        if status:

            query["status"] = status


        # Creator email
        if creator_email:

            query["created_by"] = creator_email


        # Event date
        if event_date:

            query["event_date"] = event_date


        # Participant email
        if participant_email:

            query["participants.email"] = participant_email



        return query