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



# =====================================================
#                    Event Service
# =====================================================

# This class serves as a high-level interface for managing events.
# It encapsulates the functionality of event 
# cancellation, registration, creation, updating, removal, finding
# and reading, providing a unified service for event-related operations.
class EventService:

    def __init__(self):

        self.cancellation = EventCancellation()
        self.registration = EventRegistration()
        self.creator = EventCreator()
        self.updater = EventUpdater()
        self.remover = EventRemover()
        self.finder = EventFinder()
        self.reader = EventReader()
        self.participant_reader = ParticipantEventReader()


# Create instance of the EventService to be used throughout the application.
event_service = EventService()