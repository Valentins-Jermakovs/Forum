# =====================================================
#                        Imports
# =====================================================

# Libraries:
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

# Classes:
from .query import AuditQueryBuilder

# Models
from models import AuditLog



# =====================================================
#                   Audit Exporter
# =====================================================

# This class is responsible for exporting audit logs 
# in various formats, such as CSV. 
# It provides methods to retrieve audit logs based 
# on a query and format them for download.
class AuditExporter:

    # Constructor for the AuditExporter class.
    # Initializes the query builder.
    def __init__(self):
    
        self.query_builder = AuditQueryBuilder()

    # Method to export audit logs as a CSV file based on a given query.
    async def export_csv(
        self,
        user_email: str | None = None,
        action=None,
        entity=None,
        success: bool | None = None,
        description: str | None = None
    ) -> StreamingResponse:

        # Build query using the AuditQueryBuilder
        query = self.query_builder.build(
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


        # Get logs from the database based
        logs = await (
            AuditLog
            .find(query)
            .sort(-AuditLog.created_at)
            .to_list()
        )


        # Create buffer object
        buffer = StringIO()
        # Create writer
        writer = csv.writer(
            buffer
        )

        # Write rows
        writer.writerow(
            [
                "user_email",
                "action",
                "entity",
                "description",
                "success",
                "metadata",
                "created_at"
            ]
        )

        # Write each log entry to the CSV (columns)
        for log in logs:

            writer.writerow(
                [
                    log.user_email,
                    log.action.value,
                    log.entity.value,
                    log.description,
                    log.success,
                    str(log.metadata),
                    log.created_at
                ]
            )

        # This is necessary to reset the buffer's 
        # position to the beginning before returning it in the response.
        buffer.seek(0)


        return StreamingResponse(
            buffer,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition":
                "attachment; filename=audit_logs.csv"
            }
        )