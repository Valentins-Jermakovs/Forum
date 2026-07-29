# =====================================================
#                        Imports
# =====================================================

# Models:
from models import AuditLog



# =====================================================
#                 Audit Repository
# =====================================================

# Repository responsible for
# audit log database operations.
#
# This class communicates only with MongoDB.
class AuditRepository:


    # Create new audit log document.
    async def create(
        self,
        audit_log: AuditLog
    ) -> AuditLog:


        await audit_log.insert()

        return audit_log



    # Find audit logs with pagination.
    async def find(
        self,
        query: dict,
        offset: int,
        limit: int
    ) -> tuple[list[AuditLog], int]:


        logs = await (
            AuditLog
            .find(query)
            .sort(-AuditLog.created_at)
            .skip(offset)
            .limit(limit)
            .to_list()
        )


        total = await (
            AuditLog
            .find(query)
            .count()
        )


        return logs, total



    # Find all logs without pagination.
    #
    # Used for exports.
    async def find_all(
        self,
        query: dict
    ) -> list[AuditLog]:


        return await (
            AuditLog
            .find(query)
            .sort(-AuditLog.created_at)
            .to_list()
        )



# Singleton
audit_repository = AuditRepository()