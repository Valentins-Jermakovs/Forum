# =====================================================
#                        Imports
# =====================================================

# Libraries:
from datetime import date

# Models:
from models import LibraryEvent

# Repository:
from repositories import event_repository

# Schemas:
from schemas import (
    UpcomingEventsResponse,
    PopularEventsResponse,
    EventStatisticsResponse
)



# =====================================================
#                   Event Statistics
# =====================================================

# This class is responsible for providing 
# statistics about events.
#
# Database operations are delegated to EventRepository.
# This class only handles statistics logic and response mapping.
class EventStatistics:


    # Get upcoming events
    async def get_upcoming_events(
        self,
        limit: int = 10
    ) -> UpcomingEventsResponse:


        # Get today's date
        today = date.today()


        # Build query
        query = {
            "event_date": {
                "$gte": today
            },
            "status": "active"
        }


        # Get events from repository
        events = await event_repository.find_upcoming(
            query=query,
            limit=limit
        )


        return UpcomingEventsResponse(
            items=[
                EventStatisticsResponse(
                    id=str(event.id),
                    title=event.title,
                    library=event.library,
                    event_date=event.event_date,
                    event_time=event.event_time,
                    category=event.category,
                    status=event.status,
                    capacity=event.capacity,
                    participants_count=len(
                        event.participants
                    )
                )
                for event in events
            ]
        )



    # Get popular events
    async def get_popular_events(
        self,
        limit: int = 10
    ) -> PopularEventsResponse:


        # Aggregation pipeline
        pipeline = [
            {
                "$addFields": {
                    "participants_count": {
                        "$size": "$participants"
                    }
                }
            },
            {
                "$sort": {
                    "participants_count": -1
                }
            },
            {
                "$limit": limit
            }
        ]


        # Execute aggregation through repository
        events = await event_repository.aggregate(
            pipeline
        )


        return PopularEventsResponse(
            items=[
                EventStatisticsResponse(
                    id=str(event["_id"]),
                    title=event["title"],
                    library=event["library"],
                    event_date=event["event_date"],
                    event_time=event["event_time"],
                    category=event["category"],
                    status=event["status"],
                    capacity=event["capacity"],
                    participants_count=event["participants_count"]
                )
                for event in events
            ]
        )