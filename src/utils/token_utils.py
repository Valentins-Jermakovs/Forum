# =====================================================
#                        Imports
# =====================================================
# Libraries:
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os



# =====================================================
#                   .env initialization
# =====================================================

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



# =====================================================
#                   JWT Validator
# =====================================================

class JWTValidator:

    # Constructor
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.bearer = HTTPBearer()

    # Method to validate the JWT token
    async def validate_token(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> dict:

        # Extract the token from the credentials
        token = credentials.credentials

        # Validate the token and return the payload
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

            return payload

        # Handle exceptions for expired or invalid tokens
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

    # Method to require specific roles in the JWT payload
    async def require_roles(
        self,
        roles: list[str],
        payload: dict
    ) -> dict:

        # Check if the user has any of the required roles
        # else return empty list
        user_roles = payload.get("roles", [])

        # If the user does not have any of the required roles, 
        # raise a 403 Forbidden exception
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return payload


# Create an instance of the JWTValidator class
jwt_validator = JWTValidator()


# Usage example:
# return await jwt_validator.require_roles(
#         ["admin", "librarian"],
#         payload
#     )