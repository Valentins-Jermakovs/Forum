# =====================================================
#                        Imports
# =====================================================

# Schemas:
from schemas.event import (
    EventCreate,
    EventUpdate,
    ParticipantCreate
)


# =====================================================
#                  Event Normalizer
# =====================================================

class EventNormalizer:

    # Normalize event creation data
    def normalize_create(
        self,
        data: EventCreate
    ) -> EventCreate:

        data.title = data.title.strip().lower()
        data.description = data.description.strip().lower()
        data.library = data.library.strip().lower()
        data.place = data.place.strip().lower()
        data.duration = data.duration.strip().lower()

        data.tags = [
            tag.strip().lower()
            for tag in data.tags
        ]

        return data


    # Normalize event update data
    def normalize_update(
        self,
        data: EventUpdate
    ) -> EventUpdate:

        if data.title is not None:
            data.title = data.title.strip().lower()

        if data.description is not None:
            data.description = data.description.strip().lower()

        if data.library is not None:
            data.library = data.library.strip().lower()

        if data.place is not None:
            data.place = data.place.strip().lower()

        if data.duration is not None:
            data.duration = data.duration.strip().lower()

        if data.tags is not None:
            data.tags = [
                tag.strip().lower()
                for tag in data.tags
            ]

        return data


    # Normalize participant data
    def normalize_participant(
        self,
        participant: ParticipantCreate
    ) -> ParticipantCreate:

        participant.name = participant.name.strip().lower()
        participant.email = participant.email.strip().lower()
        participant.phone = participant.phone.strip()

        return participant


# Service instance
event_normalizer = EventNormalizer()