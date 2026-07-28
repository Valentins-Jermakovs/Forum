# ===================================================
#                       Imports
# ===================================================

# Libraries:
from pydantic import (
    BaseModel, 
    Field
)


# ===================================================
#                       Schemas
# ===================================================

# System metrics response
class SystemMetricsResponse(BaseModel):

    cpu_percent: float
    memory_percent: float
    memory_used_mb: int