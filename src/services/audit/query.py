# =====================================================
#                        Imports
# =====================================================

# Models:
from models.audit import (
    AuditAction,
    AuditEntity
)

# Utils:
from utils import (
    string_normalizer,
    email_normalizer
)


# =====================================================
#                  Audit Query Builder
# =====================================================

# This class is responsible for 
# building queries to retrieve audit logs
class AuditQueryBuilder:


    def build(
        self,
        user_email: str | None = None,
        action: AuditAction | None = None,
        entity: AuditEntity | None = None,
        success: bool | None = None,
        description: str | None = None
    ) -> dict:

        # Query
        query = {}


        # --------------------------------------
        #              Normalization
        # --------------------------------------

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

        # --------------------------------------
        #               Filters
        # --------------------------------------

        # Email
        if user_email:

            query["user_email"] = user_email


        # Action
        if action:

            query["action"] = action


        # Entity
        if entity:

            query["entity"] = entity


        # Success
        if success is not None:

            query["success"] = success


        # Description (partial match)
        if description:

            query["description"] = {
                "$regex": description,
                "$options": "i"
            }


        return query