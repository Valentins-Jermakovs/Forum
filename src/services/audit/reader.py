# =====================================================
#                        Imports
# =====================================================

# Classes:
from .query import AuditQueryBuilder

# Models
from models import AuditLog


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
        **filters
    ) -> dict:

        # Build query using the AuditQueryBuilder
        query = self.query_builder.build(
            **filters
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
        return {
            "items": logs,
            "total": total,
            "offset": offset,
            "limit": limit,
            "has_more": has_more
        }