# =====================================================
#                        Imports
# =====================================================

# Schemas:
from schemas.event import (
    EventCreate,
    EventUpdate,
    ParticipantCreate
)

# Utils:
from utils import (
    string_normalizer,
    email_normalizer
)



# =====================================================
#                  Event Normalizer
# =====================================================

# This class normalize input data
class EventNormalizer:

    # Normalize event creation data
    def normalize_create(
        self,
        data: EventCreate
    ) -> EventCreate:

        # Normalize title
        data.title = string_normalizer.normalize(
            data.title
        )


        # Normalize description
        data.description = string_normalizer.normalize(
            data.description
        )


        # Normalize library
        data.library = string_normalizer.normalize(
            data.library
        )


        # Normalize place
        data.place = string_normalizer.normalize(
            data.place
        )


        # Normalize duration
        data.duration = string_normalizer.normalize(
            data.duration
        )


        # Normalize tags
        data.tags = [
            string_normalizer.normalize(tag)
            for tag in data.tags
        ]


        return data



    # Normalize event update data
    def normalize_update(
        self,
        data: EventUpdate
    ) -> EventUpdate:

        # Normalize title
        if data.title is not None:

            data.title = string_normalizer.normalize(
                data.title
            )


        # Normalize description
        if data.description is not None:

            data.description = string_normalizer.normalize(
                data.description
            )


        # Normalize library
        if data.library is not None:

            data.library = string_normalizer.normalize(
                data.library
            )


        # Normalize place
        if data.place is not None:

            data.place = string_normalizer.normalize(
                data.place
            )


        # Normalize duration
        if data.duration is not None:

            data.duration = string_normalizer.normalize(
                data.duration
            )


        # Normalize tags
        if data.tags is not None:

            data.tags = [
                string_normalizer.normalize(tag)
                for tag in data.tags
            ]


        return data



    # Normalize participant data
    def normalize_participant(
        self,
        participant: ParticipantCreate
    ) -> ParticipantCreate:

        # Normalize name
        participant.name = string_normalizer.normalize(
            participant.name
        )


        # Normalize email
        participant.email = email_normalizer.normalize(
            participant.email
        )


        # Normalize phone
        participant.phone = (
            participant.phone.strip()
        )


        return participant



# Service instance
event_normalizer = EventNormalizer()