"""Custom Authentication Class."""

from datetime import datetime, timedelta, timezone  # Import datetime related modules
from django.conf import settings  # Import Django settings
from django.contrib.auth import get_user_model  # Import Django user model
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
)  # Import JWT exceptions
from rest_framework.authentication import (
    BaseAuthentication,
)  # Import DRF BaseAuthentication
from rest_framework.exceptions import (
    AuthenticationFailed,
)  # Import DRF AuthenticationFailed
import jwt  # Import JWT library

User = get_user_model()  # Get the user model specified in Django settings


class JWTAuthentication(BaseAuthentication):
    """
    Custom authentication class using JSON Web Tokens (JWT).
    """

    def authenticate(self, request):
        """
        Authenticate the request based on the provided JWT token.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            Tuple[User, None]: A tuple of (user, None) if authentication succeeds, or None if authentication fails.
        """
        token = self.extract_token(
            request=request
        )  # Extract JWT token from the request
        if token is None:
            return None  # No token found, return None

        try:
            # Decode the token using the secret key and verify its validity
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.verify_token(payload=payload)  # Verify the token's expiration
            user_id = payload["id"]  # Extract user ID from the token payload
            user = User.objects.get(
                id=user_id
            )  # Retrieve user object from the database
            return user  # Return authenticated user
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            # Handle invalid or expired token, or user not found in the database
            raise AuthenticationFailed(detail="Invalid Token", code=400)

    def verify_token(self, payload):
        """
        Verify the JWT token's expiration.

        Args:
            payload (dict): The decoded JWT payload.

        Raises:
            InvalidTokenError: If the token has no expiration timestamp.
        """
        if "exp" not in payload:
            raise InvalidTokenError("Token has no expiration")

        exp_timestamp = payload["exp"]  # Get expiration timestamp from the payload
        current_timestamp = datetime.now(
            timezone.utc
        ).timestamp()  # Get current UTC timestamp

        # Verify if the token has expired
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        """
        Extract the JWT token from the Authorization header in the request.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            str: The JWT token extracted from the Authorization header, or None if not found.
        """
        auth_header = request.headers.get(
            "Authorization", None
        )  # Get the Authorization header
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]  # Extract the token part from the header
        return None  # Return None if no token found

    @staticmethod
    def generate_token(payload):
        """
        Generate a JWT token with the provided payload.

        Args:
            payload (dict): The payload to be encoded in the JWT token.

        Returns:
            str: The encoded JWT token.
        """
        expiration = datetime.now(timezone.utc) + timedelta(
            hours=24
        )  # Set token expiration (24 hours from now)
        payload["exp"] = expiration  # Add expiration timestamp to the payload

        # Encode the payload into a JWT token using the secret key and HS256 algorithm
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token  # Return the encoded JWT token
