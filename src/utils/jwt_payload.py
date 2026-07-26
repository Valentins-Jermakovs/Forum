# =====================================================
#                        Imports
# =====================================================

# Libraries:
from fastapi import HTTPException



# =====================================================
#                  JWT Payload
# =====================================================

# JWTPayload class is responsible for extracting user information 
# from the JWT token payload.
class JWTPayload:


    # Method to get the user email from the JWT payload
    def get_user_email(
        self,
        payload: dict
    ) -> str:

        # Get the email from the payload
        email = payload.get("email")

        # Raise an HTTPException if the email 
        # is not found in the payload
        if not email:
            raise HTTPException(
                status_code=401,
                detail="Email not found"
            )


        return email


    # Method to get the user id from the JWT payload
    def get_user_id(
        self,
        payload: dict
    ) -> str:

        # Get the user id from the payload
        user_id = payload.get("sub")

        # Raise an HTTPException if the user id
        # is not found in the payload
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="User id not found"
            )


        return user_id


    # Get the user roles from the JWT payload
    def get_roles(
        self,
        payload: dict
    ) -> list[str]:

        return payload.get(
            "roles",
            []
        )


    # Method to get the current user information from the JWT payload
    # Returns a dictionary with: 
    #   - user id, 
    #   - email, 
    #   - roles
    def get_user(
        self,
        payload: dict
    ) -> dict:

        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "roles": payload.get("roles", [])
        }


# Create an instance of the JWTPayload class
jwt_payload = JWTPayload()