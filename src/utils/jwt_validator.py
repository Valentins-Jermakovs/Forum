# =====================================================
#                        Imports
# =====================================================

# Libraries:
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv



# ====================================================
#                       .env
# ====================================================

# Load environment variables
load_dotenv()

# Secret key and algorithm for JWT validation
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



# =====================================================
#                   JWT Validator
# =====================================================

# JWTValidator class is responsible 
# for validating JWT tokens and extracting user information 
# from the token payload.
class JWTValidator:

    # Constructor
    def __init__(self):
        self.bearer = HTTPBearer()


    # Validate the JWT token and return the payload
    async def validate_token(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> dict:

        # Extract the token from the credentials
        token = credentials.credentials


        # Try to decode the token using the secret key and algorithm
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )


        # Handle exceptions for expired tokens
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )


        # Handle exceptions for invalid tokens
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )


    # Check if the user has the required roles
    async def require_roles(
        self,
        roles: list[str],
        payload: dict
    ) -> dict:

        # Get the roles from the payload
        # else return an empty list
        user_roles = payload.get(
            "roles",
            []
        )


        # Check if the user has any of the required roles
        if not any(
            role in user_roles
            for role in roles
        ):
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )


        return payload



# Create an instance of the JWTValidator class
jwt_validator = JWTValidator()