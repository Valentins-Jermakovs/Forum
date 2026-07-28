# =====================================================
#                        Imports
# =====================================================

# Libraries:
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import date, datetime
from beanie import PydanticObjectId
from enum import Enum



# =====================================================
#                         Enums
# =====================================================

# Event category Enum
class EventCategory(str, Enum):

    BOOK_PRESENTATION = "book_presentation"
    MASTER_CLASS = "master_class"
    LECTURE = "lecture"
    COMPETITION = "competition"
    EXHIBITION = "exhibition"
    DISCUSSION = "discussion"
    OTHER = "other"


# Event status Enum
class EventStatus(str, Enum):

    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



# =====================================================
#                    Participant Schemas
# =====================================================

class ParticipantCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    phone: str = Field(
        min_length=5,
        max_length=20
    )



class ParticipantResponse(ParticipantCreate):

    name: str
    email: str
    phone: str



# =====================================================
#                  Event Create Schema
# =====================================================

class EventCreate(BaseModel):

    title: str = Field(
        min_length=3,
        max_length=255
    )

    description: str = Field(
        min_length=10,
        max_length=1000
    )

    library: str = Field(
        min_length=2,
        max_length=255
    )

    place: str = Field(
        min_length=2,
        max_length=255
    )

    tags: list[str] = Field(
        default_factory=list
    )

    event_date: date
    event_time: str

    duration: str = Field(
        min_length=1,
        max_length=50
    )

    capacity: int = Field(
        ge=1
    )

    category: EventCategory



# =====================================================
#                  Event Update Schema
# =====================================================

class EventUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255
    )


    description: str | None = Field(
        default=None,
        min_length=10,
        max_length=1000
    )


    library: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )


    place: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )


    tags: list[str] | None = None
    event_date: date | None = None
    event_time: str | None = None


    duration: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


    capacity: int | None = Field(
        default=None,
        ge=1
    )


    category: EventCategory | None = None
    status: EventStatus | None = None



# =====================================================
#              Register Participant Schema
# =====================================================

class RegisterParticipantRequest(BaseModel):

    participant: ParticipantCreate


# =====================================================
#                   Event Response
# =====================================================

class EventResponse(BaseModel):

    id: PydanticObjectId

    title: str
    description: str
    library: str
    place: str
    tags: list[str]

    event_date: date
    event_time: str
    duration: str

    capacity: int
    participants: list[ParticipantResponse]

    category: EventCategory
    status: EventStatus

    created_by: str
    created_at: datetime
    updated_at: datetime


# =====================================================
#                Pagination Response
# =====================================================

class EventsResponse(BaseModel):

    items: list[EventResponse]

    total: int
    offset: int
    limit: int
    has_more: bool



# =====================================================
#             Event Statistics Response
# =====================================================


# Short event representation for statistics
class EventStatisticsResponse(BaseModel):

    id: PydanticObjectId

    title: str
    library: str
    event_date: date
    event_time: str
    category: EventCategory
    status: EventStatus
    capacity: int
    participants_count: int = 0



# =====================================================
#          Upcoming Events Response
# =====================================================


class UpcomingEventsResponse(BaseModel):

    items: list[EventStatisticsResponse]



# =====================================================
#          Popular Events Response
# =====================================================


class PopularEventsResponse(BaseModel):

    items: list[EventStatisticsResponse]