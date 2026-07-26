# ===================================================
#                       Imports
# ===================================================

# Libraries:
from pydantic import BaseModel, Field


# ===================================================
#                       Schemas
# ===================================================

# System metrics response
class SystemMetricsResponse(BaseModel):

    # CPU usage percentage
    cpu_percent: float = Field(
        description="CPU usage percentage"
    )

    # Memory usage percentage
    memory_percent: float = Field(
        description="Memory usage percentage"
    )

    # Used memory in megabytes
    memory_used_mb: int = Field(
        description="Used memory in MB"
    )