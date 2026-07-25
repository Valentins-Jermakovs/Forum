# =====================================================
#                        Imports
# =====================================================

# Librairies:
from typing import Any

# Models:
from models.audit import (
    AuditAction,
    AuditEntity,
    AuditLog
)



# =====================================================
#                     Audit Writer
# =====================================================

# This class is responsible for writing audit logs to the database.
class AuditWriter:


    async def create_log(
        self,
        user_email: str,
        action: AuditAction,
        entity: AuditEntity,
        description: str,
        success: bool = True,
        metadata: dict[str, Any] | None = None
    ) -> AuditLog:

        # Create an instance of the AuditLog 
        # model with the provided data.
        audit_log = AuditLog(
            user_email=user_email,
            action=action,
            entity=entity,
            description=description,
            success=success,
            metadata=metadata or {}
        )

        # Save the audit log to the database.
        await audit_log.insert()

        # Return the created audit log instance.
        return audit_log