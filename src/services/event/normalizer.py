# =====================================================
#                        Imports
# =====================================================

# Libraries:
from datetime import datetime
from fastapi import HTTPException

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


    # Normalize simple string values
    def normalize_string(
        self,
        string: str
    ) -> str:

        return string.strip().lower()


    # Normalize date values
    def normalize_date(
        self,
        date: str
    ) -> datetime:

        try:

            return datetime.strptime(
                date.strip(),
                "%Y-%m-%d"
            )

        except ValueError:

            raise HTTPException(
                status_code=400,
                detail="Invalid event date format. Use YYYY-MM-DD"
            )


    # Normalize email values
    def normalize_email(
        self,
        email: str
    ) -> str:

        return email.strip().lower()



    # Normalize event creation data
    def normalize_create(
        self,
        data: EventCreate
    ) -> EventCreate:


        data.title = self.normalize_string(
            data.title
        )

        data.description = self.normalize_string(
            data.description
        )

        data.library = self.normalize_string(
            data.library
        )

        data.place = self.normalize_string(
            data.place
        )

        data.duration = self.normalize_string(
            data.duration
        )


        data.tags = [
            self.normalize_string(tag)
            for tag in data.tags
        ]


        return data



    # Normalize event update data
    def normalize_update(
        self,
        data: EventUpdate
    ) -> EventUpdate:


        if data.title is not None:

            data.title = self.normalize_string(
                data.title
            )


        if data.description is not None:

            data.description = self.normalize_string(
                data.description
            )


        if data.library is not None:

            data.library = self.normalize_string(
                data.library
            )


        if data.place is not None:

            data.place = self.normalize_string(
                data.place
            )


        if data.duration is not None:

            data.duration = self.normalize_string(
                data.duration
            )


        if data.tags is not None:

            data.tags = [
                self.normalize_string(tag)
                for tag in data.tags
            ]


        return data



    # Normalize participant data
    def normalize_participant(
        self,
        participant: ParticipantCreate
    ) -> ParticipantCreate:


        participant.name = self.normalize_string(
            participant.name
        )


        participant.email = self.normalize_email(
            participant.email
        )


        participant.phone = (
            participant.phone.strip()
        )


        return participant



# Service instance
event_normalizer = EventNormalizer()