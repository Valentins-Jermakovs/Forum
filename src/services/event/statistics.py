# =====================================================
#                        Imports
# =====================================================

# Libraries
from datetime import date

# Models:
from models import LibraryEvent

# Schemas
from schemas import(
    UpcomingEventsResponse,
    PopularEventsResponse,
    EventStatisticsResponse
)

# =====================================================
#                   Event Statistics
# =====================================================

# This class is responsible for providing 
# statistics about events, such as upcoming events 
# and popular events.
class EventStatistics:

    # Get Upcoming Events - retrieves a list of upcoming events
    async def get_upcoming_events(
        self,
        limit: int = 10
    ) -> UpcomingEventsResponse:

        # Get today's date to filter events 
        # that are scheduled for today or later.
        today = date.today()


        # Query the database for events that are scheduled
        # for today or later and have an "active" status.
        events = await (
            LibraryEvent
            .find(
                {
                    "event_date": {
                        "$gte": today
                    },
                    "status": "active"
                }
            )
            .sort(
                LibraryEvent.event_date
            )
            .limit(limit)
            .to_list()
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


    # Method to get popular events 
    # based on the number of participants.
    async def get_popular_events(
        self,
        limit: int = 10
    ) -> PopularEventsResponse:

        # Define an aggregation pipeline 
        # to calculate the number of participants
        # and sort the events by this count in descending order.
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


        # Execute the aggregation pipeline and return the results.
        events = await LibraryEvent.aggregate(
            pipeline
        ).to_list()


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