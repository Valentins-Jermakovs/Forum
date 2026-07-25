# =====================================================
#                   Event Query Builder
# =====================================================

# Models:
from models.event import (
    EventCategory,
    EventStatus
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

        creator_id: int | None = None,

        event_date: str | None = None,

        participant_email: str | None = None

    ) -> dict:

        # Query
        query = {}


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

        # Creator ID
        if creator_id:

            query["creator_id"] = creator_id

        # Event date
        if event_date:

            query["event_date"] = event_date

        # Participiant email
        if participant_email:

            query["participants.email"] = participant_email


        return query