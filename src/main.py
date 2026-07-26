# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Config:
from config.database import init_db

# Routes
from api import main_router



# =====================================================
#                  Application lifespan
# =====================================================

# This function runs on app startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Initialize database when application starts
    await init_db()
    # Application works while this yield exists
    yield



# =====================================================
#                   FastAPI application
# =====================================================

# Create FastAPI app with custom lifespan logic
app = FastAPI(lifespan=lifespan)

# Router object for all API routes
app.include_router(main_router)