"""
Login Module - User Authentication
Author: dakezard
Date: 2026-05-02

This module handles user authentication including:
- Username/password validation
- JWT token generation
- Session management
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import secrets

SECRET_KEY = "your-secret-key-here"  # Should be from config
TOKEN_EXPIRY_HOURS = 24


class AuthenticationService:
    """Handles all authentication related operations"""

    def __init__(self, db_session):
        self.db = db_session

    def hash_password(self, plain_password: str) -> str:
        """
        Hash password using bcrypt with salt

        Args:
            plain_password: Plain text password

        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash

        Args:
            plain_password: Plain text password to check
            hashed_password: Stored hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            print(f"Password verification error: {e}")
            return False

    def generate_token(self, user_id: int, username: str) -> str:
        """
        Generate JWT token for authenticated user

        Args:
            user_id: User's database ID
            username: User's username

        Returns:
            JWT token string
        """
        payload = {
            'user_id': user_id,
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS),
            'iat': datetime.utcnow(),
            'jti': secrets.token_urlsafe(16)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token

        Args:
            token: JWT token string

        Returns:
            Decoded payload dict if valid, None if invalid/expired
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """
        Main authentication method

        Args:
            username: User's username
            password: User's password

        Returns:
            Dict with user info and token if successful, None if failed
        """
        # Query user from database (pseudo-code)
        user = self.db.query_user(username)

        if not user:
            return None

        if not self.verify_password(password, user.password_hash):
            return None

        token = self.generate_token(user.id, user.username)

        return {
            'user_id': user.id,
            'username': user.username,
            'token': token,
            'expires_in': TOKEN_EXPIRY_HOURS * 3600
        }


if __name__ == '__main__':
    # Test the authentication service
    auth = AuthenticationService(db_session=None)

    # Test password hashing
    password = "securePassword123!"
    hashed = auth.hash_password(password)
    print(f"Hashed password: {hashed[:20]}...")

    # Test password verification
    is_valid = auth.verify_password(password, hashed)
    print(f"Password valid: {is_valid}")

    print("\n✅ Login module implementation complete!")
