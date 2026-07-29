# =====================================================
#                        Imports
# =====================================================

# Libraries:
import csv
from io import StringIO


# Models:
from models import AuditLog



# =====================================================
#                 Audit Exporter
# =====================================================

# Responsible only for converting
# audit logs into export formats.
class AuditExporter:


    def export_csv(
        self,
        logs: list[AuditLog]
    ) -> StringIO:


        buffer = StringIO()


        writer = csv.writer(
            buffer
        )


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


        buffer.seek(0)


        return buffer


# Global instance
audit_exporter = AuditExporter()