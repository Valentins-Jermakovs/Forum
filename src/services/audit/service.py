# =====================================================
#                        Imports
# =====================================================

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


    def __init__(self):

        self.writer = AuditWriter()
        self.reader = AuditReader()
        self.exporter = AuditExporter()


# Create instance of the AuditService to be used throughout the application.
audit_service = AuditService()