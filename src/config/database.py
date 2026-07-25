# =====================================================
#                        Imports
# =====================================================

# Libraries:
from pymongo import AsyncMongoClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

# Models:
from models import AuditLog, LibraryEvent



# ====================================================
#                       Database
# ====================================================

# Load environment variables
load_dotenv()


# ====================================================
#           Initialize Database Connection
# ====================================================

async def init_db():

    # Connect to database
    client = AsyncMongoClient(os.getenv("MONGO_URL"))
    db = client[os.getenv("DB_NAME")]

    await init_beanie(
        database=db, 
        document_models=[
            AuditLog, 
            LibraryEvent
        ]
    )