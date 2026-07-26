# =====================================================
#                        Imports
# =====================================================

# Libraries:
import psutil
from fastapi import APIRouter, Depends

# Schemas
from schemas import SystemMetricsResponse

# Utils
from utils.jwt_validator import jwt_validator



# Router object
router = APIRouter(
    prefix="/metrics",
    tags=["Metrics services"],
)



# =====================================================
#                       Endpoints
# =====================================================

# Endpoint for getting metrics
@router.get(
    "/stats",
    response_model=SystemMetricsResponse,
    summary="Get current system metrics"
)
async def metrics(
    payload = Depends(jwt_validator.validate_token),
) -> SystemMetricsResponse:

    # Admin role check
    await jwt_validator.require_roles(
        roles=["admin"],
        payload=payload
    )


    # Return current system metrics
    return {
        # CPU usage percentage
        "cpu_percent": psutil.cpu_percent(),
        # Memory usage percentage
        "memory_percent": psutil.virtual_memory().percent,
        # Used memory in megabytes
        "memory_used_mb": round(psutil.virtual_memory().used / 1024 / 1024),
    }