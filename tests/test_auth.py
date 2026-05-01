import pytest
from auth_service import hash_password, verify_token

class TestAuthService:
    def test_hash_password(self):
        """Test password hashing produces consistent results"""
        password = "test_password_123"
        hashed = hash_password(password)
        assert hashed is not None
        assert isinstance(hashed, bytes)

    def test_verify_valid_token(self):
        """Test verification of valid JWT token"""
        valid_token = generate_test_token(user_id=1)
        payload = verify_token(valid_token)
        assert payload is not None
        assert payload['user_id'] == 1

    def test_verify_expired_token(self):
        """Test that expired tokens are rejected"""
        expired_token = generate_expired_token()
        assert verify_token(expired_token) is None

    def test_password_verification(self):
        """Test that correct passwords can be verified"""
        password = "secure_password"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False
