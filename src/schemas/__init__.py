# =======This file is used to export all schemas=======

# =====================================================
#                        Imports
# =====================================================

from .event import (
    EventCategory,
    EventStatus,
    ParticipantCreate,
    ParticipantResponse,
    EventCreate,
    EventUpdate,
    RegisterParticipantRequest,
    EventResponse,
    EventsResponse,
    EventStatisticsResponse,
    UpcomingEventsResponse,
    PopularEventsResponse
)

from .audit import (
    AuditAction,
    AuditEntity,
    AuditLogResponse,
    AuditLogsResponse
)