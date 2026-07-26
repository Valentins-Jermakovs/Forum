# =====================================================
#                        Imports
# =====================================================

# Classes:
from .query import AuditQueryBuilder

# Models
from models import AuditLog

# Schemas
from schemas import (
    AuditAction, 
    AuditEntity,
    AuditLogsResponse,
    AuditLogResponse
)

# =====================================================
#                     Audit Reader
# =====================================================

# This class is responsible for reading audit logs from the database
# using the AuditQueryBuilder to construct queries based on provided filters.
class AuditReader:

    # Constructor for the AuditReader class. 
    # Initializes the query builder.
    def __init__(self):

        self.query_builder = AuditQueryBuilder()



    async def get_logs(
        self,
        offset: int = 0,
        limit: int = 20,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ) -> dict:

        # Build query using the AuditQueryBuilder
        query = self.query_builder.build(
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


        # Get logs from the database based 
        # on the constructed query, with pagination.
        logs = await (
            AuditLog
            .find(query)
            .sort(-AuditLog.created_at)
            .skip(offset)
            .limit(limit)
            .to_list()
        )


        # Count the total number of logs 
        # that match the query for pagination purposes.
        total = await (
            AuditLog
            .find(query)
            .count()
        )

        # Determine if there are more logs 
        # available beyond the current page.
        has_more = offset + limit < total

        # Return the logs along with pagination information.
        return AuditLogsResponse(
            items=[
                AuditLogResponse(
                    id=str(log.id),
                    user_email=log.user_email,
                    action=log.action,
                    entity=log.entity,
                    description=log.description,
                    success=log.success,
                    metadata=log.metadata,
                    created_at=log.created_at
                )
                for log in logs
            ],
            total=total,
            offset=offset,
            limit=limit,
            has_more=has_more
        )