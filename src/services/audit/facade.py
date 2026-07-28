# =====================================================
#                        Imports
# =====================================================

# Libraries:
from typing import Any

# Models:
from models import (
    AuditAction,
    AuditEntity,
    AuditLog
)

# Schemas
from schemas import AuditLogsResponse

# Classes:
from .writer import AuditWriter
from .reader import AuditReader
from .exporter import AuditExporter



# =====================================================
#                     Audit Service
# =====================================================

# This class serves as a high-level interface for managing audit logs.
# It encapsulates the functionality of writing, reading, and exporting audit logs,
# providing a unified service for audit-related operations.
class AuditService:

    # Constructor - initialize classes
    def __init__(self):

        self._writer = AuditWriter()
        self._reader = AuditReader()
        self._exporter = AuditExporter()


    # Method - write log
    async def create_log(
        self,
        user_email: str,
        action: AuditAction,
        entity: AuditEntity,
        description: str,
        success: bool = True,
        metadata: dict[str, Any] | None = None
    ) -> AuditLog:


        return await self._writer.create_log(
            user_email=user_email,
            action=action,
            entity=entity,
            description=description,
            success=success,
            metadata=metadata
        )


    # Method for getting logs
    async def get_logs(
        self,
        offset: int = 0,
        limit: int = 20,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ) -> AuditLogsResponse:


        return await self._reader.get_logs(
            offset=offset,
            limit=limit,
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


    # Method for exporting logs in csv file
    async def export_csv(
        self,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ):

        
        return await self._exporter.export_csv(
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


# Create instance of the AuditService to be used throughout the application.
audit_service = AuditService()