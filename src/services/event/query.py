# =====================================================
#                   Event Query Builder
# =====================================================

# Libraries:
from datetime import datetime

# Models:
from models.event import (
    EventCategory,
    EventStatus
)

# Classes:
from .normalizer import event_normalizer

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
        #               Filters
        # --------------------------------------

        # Normalize strings
        if title:
            title = event_normalizer.normalize_string(
                title
            )


        if library:
            library = event_normalizer.normalize_string(
                library
            )


        if creator_email:
            creator_email = event_normalizer.normalize_email(
                creator_email
            )


        if participant_email:
            participant_email = event_normalizer.normalize_email(
                participant_email
            )

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
        if creator_email:

            query["created_by"] = {
                "$regex": creator_email,
                "$options": "i"
            }

        # Event date
        if event_date:

            event_date = event_normalizer.normalize_date(
                event_date
            )

            query["event_date"] = event_date

        # Participant email
        if participant_email:

            query["participants.email"] = {
                "$regex": participant_email,
                "$options": "i"
            }


        return query