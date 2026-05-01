"""
Unit Tests for Authentication Bug Fix
Author: dakezard
Date: 2026-05-02
"""

import pytest
import jwt
from datetime import datetime, timedelta
import sys
sys.path.insert(0, 'src/middleware')

from auth_fix import (
    TokenValidator,
    AuthenticationError,
    require_auth
)


class TestTokenValidator:
    """Test suite for enhanced token validation"""

    @pytest.fixture
    def validator(self):
        return TokenValidator(secret_key='test-secret-key')

    @pytest.fixture
    def valid_token(self, validator):
        """Generate a valid token for testing"""
        payload = {
            'user_id': 42,
            'username': 'testuser',
            'exp': datetime.utcnow() + timedelta(hours=1),
            'iat': datetime.utcnow(),
            'jti': 'test-token-id-123'
        }
        return jwt.encode(payload, validator.secret_key, algorithm='HS256')

    def test_valid_token_validation(self, validator, valid_token):
        """Test that valid tokens are accepted"""
        result = validator.validate_token(valid_token)

        assert result['user_id'] == 42
        assert result['username'] == 'testuser'
        assert 'exp' in result
        print("✓ Valid token accepted")

    def test_missing_token_raises_error(self, validator):
        """Test that missing tokens are rejected properly"""
        with pytest.raises(AuthenticationError) as exc_info:
            validator.validate_token(None)

        assert exc_info.value.error_code == 'TOKEN_MISSING'
        assert exc_info.value.status_code == 401
        print("✓ Missing token raises correct error")

    def test_expired_token_handling(self, validator):
        """Test that expired tokens are handled gracefully"""
        expired_payload = {
            'user_id': 42,
            'username': 'testuser',
            'exp': datetime.utcnow() - timedelta(hours=1),  # Already expired
            'iat': datetime.utcnow() - timedelta(hours=2),
            'jti': 'expired-token-id'
        }

        expired_token = jwt.encode(
            expired_payload,
            validator.secret_key,
            algorithm='HS256'
        )

        with pytest.raises(AuthenticationError) as exc_info:
            validator.validate_token(expired_token)

        assert exc_info.value.error_code == 'TOKEN_EXPIRED'
        assert 'expired' in exc_info.value.message.lower()
        print("✓ Expired token handled correctly")

    def test_invalid_token_format(self, validator):
        """Test that malformed tokens are rejected"""
        invalid_tokens = [
            "not.a.valid.token",
            "",
            "bearer sometoken",
            "12345",
            "eyJhbGciOiJIUzI1NiJ9",  # Incomplete base64
        ]

        for token in invalid_tokens:
            with pytest.raises(AuthenticationError):
                validator.validate_token(token)

        print(f"✓ All {len(invalid_tokens)} invalid formats rejected")

    def test_missing_payload_fields(self, validator):
        """Test rejection of tokens with incomplete payload"""
        incomplete_payload = {
            'user_id': 42
            # Missing: username, exp, iat
        }

        incomplete_token = jwt.encode(
            incomplete_payload,
            validator.secret_key,
            algorithm='HS256'
        )

        with pytest.raises(AuthenticationError) as exc_info:
            validator.validate_token(incomplete_token)

        assert exc_info.value.error_code == 'INVALID_PAYLOAD'
        print("✓ Incomplete payload rejected")

    def test_error_code_uniqueness(self, validator):
        """Verify each error scenario returns unique code"""
        error_scenarios = [
            (None, 'TOKEN_MISSING'),
            ("invalid", 'TOKEN_INVALID'),
            ("expired_token_here", 'TOKEN_EXPIRED'),  # Will fail decode
        ]

        error_codes = set()

        for token, expected_code in error_scenarios:
            try:
                validator.validate_token(token)
            except AuthenticationError as e:
                error_codes.add(e.error_code)

        # Should have at least 3 unique error codes
        assert len(error_codes) >= 3
        print(f"✓ Found {len(error_codes)} unique error codes")


if __name__ == '__main__':
    pytest.main([__file__, "-v"])
