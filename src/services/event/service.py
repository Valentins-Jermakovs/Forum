# =====================================================
#                        Imports
# =====================================================

# Classes:
from .cancel_registration import EventCancellation
from .register import EventRegistration
from .creator import EventCreator
from .updater import EventUpdater
from .remover import EventRemover
from .finder import EventFinder
from .reader import EventReader
from .participant_reader import ParticipantEventReader
from .statistics import EventStatistics

# Schemas
from schemas import (
    EventCreate, 
    EventUpdate, 
    ParticipantCreate,
    UpcomingEventsResponse,
    PopularEventsResponse,
    EventsResponse
)

# Models:
from models import (
    LibraryEvent, 
    EventCategory, 
    EventStatus
)



# =====================================================
#                    Event Service
# =====================================================

# This class serves as a high-level interface for managing events.
# It encapsulates the functionality of event 
# cancellation, registration, creation, updating, removal, finding
# and reading, providing a unified service for event-related operations.
class EventService:

    # Constructor - initializes the various event management components.
    def __init__(self):

        self._cancellation = EventCancellation()
        self._registration = EventRegistration()
        self._creator = EventCreator()
        self._updater = EventUpdater()
        self._remover = EventRemover()
        self._finder = EventFinder()
        self._reader = EventReader()
        self._participant_reader = ParticipantEventReader()
        self._statistics = EventStatistics()


    # Create a new event with the provided data, user ID, and user email.
    async def create(
        self,
        data: EventCreate,
        user_id: str,
        user_email: str
    ) -> LibraryEvent:

        return await self._creator.create(
            data=data,
            user_id=user_id,
            user_email=user_email
        )


    # Update an existing event with the provided data, user ID, and user email.
    async def update(
        self,
        event: LibraryEvent,
        data: EventUpdate,
        user_id: str,
        user_email: str,
        user_roles: list[str]
    ) -> LibraryEvent:

        return await self._updater.update(
            event=event,
            data=data,
            user_id=user_id,
            user_email=user_email,
            user_roles=user_roles
        )


    # Delete an event with the provided event, user ID, and user email.
    async def delete(
        self,
        event: LibraryEvent,
        user_id: int,
        user_email: str,
        user_roles: list[str]
    ) -> dict:

        return await self._remover.delete(
            event=event,
            user_id=user_id,
            user_email=user_email,
            user_roles=user_roles
        )


    # Register a participant for an event 
    # with the provided event and participant data.
    async def register(
        self,
        event: LibraryEvent,
        participant: ParticipantCreate,
        email: str
    ) -> LibraryEvent:

        return await self._registration.register(
            event=event,
            participant=participant,
            email=email
        )


    # Cancel a participant's registration for an event 
    # with the provided event and participant email.
    async def cancel_registration(
        self,
        event: LibraryEvent,
        email: str
    ) -> LibraryEvent:

        return await self._cancellation.cancel(
            event=event,
            email=email
        )


    # Find an event by its ID and return the corresponding LibraryEvent object.
    async def find_by_id(
        self,
        event_id: str
    ) -> LibraryEvent:

        return await self._finder.get_by_id(
            event_id=event_id
        )


    # Get a list of events based on the provided filters, offset, and limit.
    async def get(
        self,
        offset: int = 0,
        limit: int = 20,
        title: str | None = None,
        library: str | None = None,
        category: EventCategory | None = None,
        status: EventStatus | None = None,
        creator_email: str | None = None,
        event_date: str | None = None,
        participant_email: str | None = None
    ) -> EventsResponse:

        return await self._reader.get_events(
            offset=offset,
            limit=limit,
            title=title,
            library=library,
            category=category,
            status=status,
            creator_email=creator_email,
            event_date=event_date,
            participant_email=participant_email
        )


    # Get a list of events that a participant has registered for,
    async def get_user_events(
        self,
        email: str,
        offset: int = 0,
        limit: int = 20
    ) -> EventsResponse:

        return await self._participant_reader.get_registered_events(
            email=email,
            offset=offset,
            limit=limit
        )


    # Get a list of upcoming events that are scheduled 
    # for today or later, limited by the specified number.
    async def get_upcoming_events(
        self,
        limit: int = 10
    ) -> UpcomingEventsResponse:

        return await self._statistics.get_upcoming_events(
            limit=limit
        )

    
    # Get a list of popular events based on the number 
    # of participants, limited by the specified number.
    async def get_popular_events(
        self,
        limit: int = 10
    ) -> PopularEventsResponse:

        return await self._statistics.get_popular_events(
            limit=limit
        )


# Create instance of the EventService to be used throughout the application.
event_service = EventService()