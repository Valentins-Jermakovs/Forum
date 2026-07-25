# =====================================================
#                        Imports
# =====================================================

# Libraries:
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from typing import Any



# =====================================================
#                         Enums
# =====================================================

# Actions
class AuditAction(str, Enum):

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    REGISTER = "register"
    CANCEL_REGISTRATION = "cancel_registration"



# Entities
class AuditEntity(str, Enum):

    EVENT = "event"



# =====================================================
#                    Audit Response
# =====================================================

class AuditLogResponse(BaseModel):

    id: str

    user_email: str
    action: AuditAction
    entity: AuditEntity
    description: str
    success: bool
    metadata: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )



# =====================================================
#                Pagination Response
# =====================================================

class AuditLogsResponse(BaseModel):

    items: list[AuditLogResponse]

    total: int
    offset: int
    limit: int
    has_more: bool