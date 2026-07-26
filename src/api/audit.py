# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

# Schemas
from schemas import (
    AuditAction,
    AuditEntity,
    AuditLogsResponse
)

# Utils
from utils import jwt_validator

# Services
from services import audit_service



# Router object
router = APIRouter(
    prefix="/audit",
    tags=["Audit services - logs and exports"],
)



# =====================================================
#                       Endpoints
# =====================================================


# Get audit logs
@router.get(
    "/logs",
    response_model=AuditLogsResponse,
    summary="Get audit logs"
)
async def get_audit_logs(
    offset: int = 0,
    limit: int = 20,
    user_email: str | None = None,
    action: AuditAction | None = None,
    entity: AuditEntity | None = None,
    success: bool | None = None,
    description: str | None = None,
    payload = Depends(jwt_validator.validate_token)
) -> AuditLogsResponse:


    # Admin access only
    await jwt_validator.require_roles(
        roles=["admin"],
        payload=payload
    )

    # Get logs
    logs = await audit_service.get_logs(
        offset=offset,
        limit=limit,
        user_email=user_email,
        action=action,
        entity=entity,
        success=success,
        description=description
    )


    return logs


# Export audit logs to CSV
@router.get(
    "/export",
    summary="Export audit logs to CSV"
)
async def export_audit_logs(
    user_email: str | None = None,
    action: AuditAction | None = None,
    entity: AuditEntity | None = None,
    success: bool | None = None,
    description: str | None = None,
    payload = Depends(jwt_validator.validate_token)
):


    # Admin access only
    await jwt_validator.require_roles(
        roles=["admin"],
        payload=payload
    )

    # Create file
    csv_file = await audit_service.export_csv(
        user_email=user_email,
        action=action,
        entity=entity,
        success=success,
        description=description
    )

    # Return it
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={
            "Content-Disposition": 
            "attachment; filename=audit_logs.csv"
        }
    )