# =====================================================
#                        Imports
# =====================================================

# Models:
from models import LibraryEvent



# =====================================================
#                 Event Repository
# =====================================================

# Repository responsible for
# database operations related to events.
#
# This class only works with MongoDB.
# Business logic stays inside services.
class EventRepository:



    # Find event by id
    async def find_by_id(
        self,
        event_id: str
    ) -> LibraryEvent | None:


        return await LibraryEvent.get(
            event_id
        )



    # Create event
    async def create(
        self,
        event: LibraryEvent
    ) -> LibraryEvent:


        await event.insert()

        return event



    # Save existing event
    async def save(
        self,
        event: LibraryEvent
    ) -> LibraryEvent:


        await event.save()

        return event



    # Delete event
    async def delete(
        self,
        event: LibraryEvent
    ) -> None:


        await event.delete()



    # Search events
    async def search(
        self,
        query: dict,
        offset: int,
        limit: int,
        sort=None
    ) -> tuple[list[LibraryEvent], int]:


        result = (
            LibraryEvent
            .find(query)
        )


        if sort:

            result = result.sort(sort)


        events = await (
            result
            .skip(offset)
            .limit(limit)
            .to_list()
        )


        total = await (
            LibraryEvent
            .find(query)
            .count()
        )


        return events, total



    # Find events for statistics
    async def find_upcoming(
        self,
        query: dict,
        limit: int
    ) -> list[LibraryEvent]:


        return await (
            LibraryEvent
            .find(query)
            .sort(
                LibraryEvent.event_date
            )
            .limit(limit)
            .to_list()
        )



    # Aggregation statistics
    async def aggregate(
        self,
        pipeline: list
    ) -> list:


        return await (
            LibraryEvent
            .aggregate(
                pipeline
            )
            .to_list()
        )



    # Check event uniqueness
    async def find_existing(
        self,
        query: dict
    ) -> LibraryEvent | None:


        return await (
            LibraryEvent
            .find_one(query)
        )


# Singleton
event_repository = EventRepository()