# =====================================================
#                        Imports
# =====================================================

# Libraries:
from typing import Any


# Models:
from models import (
    AuditLog,
    AuditAction,
    AuditEntity
)


# Schemas:
from schemas import (
    AuditLogsResponse,
    AuditLogResponse
)


# Repository:
from repositories import audit_repository


# Classes:
from .audit_exporter import audit_exporter

# Utils:
from utils import audit_query_builder


# =====================================================
#                    Audit Service
# =====================================================

class AuditService:


    # Create audit log
    async def create_log(
        self,
        user_email: str,
        action: AuditAction,
        entity: AuditEntity,
        description: str,
        success: bool = True,
        metadata: dict[str, Any] | None = None
    ) -> AuditLog:


        log = AuditLog(
            user_email=user_email,
            action=action,
            entity=entity,
            description=description,
            success=success,
            metadata=metadata or {}
        )


        return await audit_repository.create(
            log
        )



    # Get logs
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



        query = audit_query_builder.build(
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


        logs, total = await audit_repository.find(
            query=query,
            offset=offset,
            limit=limit
        )


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
            has_more=offset + limit < total
        )



    # Export CSV
    async def export_csv(
        self,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ):


        query = audit_query_builder.build(
            user_email=user_email,
            action=action,
            entity=entity,
            success=success,
            description=description
        )


        logs = await audit_repository.find_all(
            query
        )


        return audit_exporter.export_csv(
            logs
        )



# Singleton
audit_service = AuditService()