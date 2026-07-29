# =====================================================
#                        Imports
# =====================================================

# Models:
from models import (
    AuditAction,
    AuditEntity
)


# Utils:
from utils import (
    string_normalizer,
    email_normalizer
)



# =====================================================
#              Audit Query Builder
# =====================================================

class AuditQueryBuilder:


    def build(
        self,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ) -> dict:


        query = {}


        # Normalize email
        if user_email:

            user_email = email_normalizer.normalize(
                user_email
            )


        # Normalize description
        if description:

            description = string_normalizer.normalize(
                description
            )



        # Filters

        if user_email:

            query["user_email"] = user_email



        if action:

            query["action"] = action



        if entity:

            query["entity"] = entity



        if success is not None:

            query["success"] = success



        if description:

            query["description"] = {
                "$regex": description,
                "$options": "i"
            }


        return query


# Global instance
audit_query_builder = AuditQueryBuilder()