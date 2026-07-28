# =====================================================
#                        Imports
# =====================================================

# Libraries:
from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from datetime import date, time, datetime
from enum import Enum



# =====================================================
#                         Enums
# =====================================================

# EventCategory Enum
class EventCategory(str, Enum):

    BOOK_PRESENTATION = "book_presentation"
    MASTER_CLASS = "master_class"
    LECTURE = "lecture"
    COMPETITION = "competition"
    EXHIBITION = "exhibition"
    DISCUSSION = "discussion"
    OTHER = "other"


# EventStatus Enum
class EventStatus(str, Enum):

    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



# =====================================================
#                    Participant Model
# =====================================================

# Participant Model
class Participant(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr
    phone: str



# =====================================================
#                     Event Model
# =====================================================

class LibraryEvent(Document):

    # Basic information

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: str        # Description of the event
    library: str            # Library
    place: str              # "Cabinet 205, 2nd floor"

    # Search tags
    tags: list[str] = Field(
        default_factory=list
    )


    # Date and time
    event_date: date
    event_time: str
    duration: str   # 2 hours, 30 minutes, etc.


    # Maximum number of participants
    capacity: int = Field(
        ge=0
    )
    # Registered users
    participants: list[Participant] = Field(
        default_factory=list
    )


    category: EventCategory # Event category
    status: EventStatus = EventStatus.ACTIVE    # Event status


    # Who created event
    creator_id: str
    created_by: str


    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.now
    )
    updated_at: datetime = Field(
        default_factory=datetime.now
    )


    # Collection name
    class Settings:
        name = "library_events"