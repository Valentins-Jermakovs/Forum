# =====================================================
#                        Imports
# =====================================================

# Libraries:
from beanie import Document
from pydantic import Field
from datetime import datetime
from enum import Enum
from typing import Optional, Any



# =====================================================
#                         Enums
# =====================================================

# Actions
class AuditAction(str, Enum):

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    REGISTER = "register"
    CANCEL = "cancel"

    LOGIN = "login"
    LOGOUT = "logout"


# Entities
class AuditEntity(str, Enum):

    EVENT = "event"
    USER = "user"



# =====================================================
#                     Audit Model
# =====================================================

class AuditLog(Document):

    # User who performed action
    user: Optional[str] = None

    # Action type
    action: AuditAction

    # Target entity
    entity: AuditEntity

    # Description
    description: str

    # Was operation successful
    success: bool = True

    # Additional information
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    # Creation time
    created_at: datetime = Field(
        default_factory=datetime.now
    )

    # Collection name
    class Settings:
        name = "audit_logs"