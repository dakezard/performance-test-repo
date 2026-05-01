"""
Authentication Middleware for FastAPI
Author: dakezard
Date: 2026-05-02

Provides middleware for protecting routes with JWT authentication
"""

from functools import wraps
from flask import request, jsonify, g
import jwt
from datetime import datetime


class AuthMiddleware:
    """Middleware class for JWT authentication"""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def token_required(self, f):
        """
        Decorator to require valid JWT token for endpoint

        Usage:
            @app.route('/protected')
            @auth.token_required
            def protected_route():
                return {'message': 'This is protected'}
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            # Check for token in Authorization header
            if 'Authorization' in request.headers:
                auth_header = request.headers['Authorization']
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]

            if not token:
                return jsonify({
                    'error': 'Token is missing',
                    'code': 'AUTH_001'
                }), 401

            try:
                # Decode and verify token
                payload = jwt.decode(
                    token,
                    self.secret_key,
                    algorithms=['HS256']
                )

                # Store user info in Flask g object
                g.current_user_id = payload['user_id']
                g.current_username = payload['username']
                g.token_issued_at = datetime.fromtimestamp(payload['iat'])

            except jwt.ExpiredSignatureError:
                return jsonify({
                    'error': 'Token has expired',
                    'code': 'AUTH_002'
                }), 401

            except jwt.InvalidTokenError as e:
                return jsonify({
                    'error': f'Invalid token: {str(e)}',
                    'code': 'AUTH_003'
                }), 401

            return f(*args, **kwargs)

        return decorated

    def admin_required(self, f):
        """
        Decorator requiring admin role in addition to valid token
        """
        @wraps(f)
        def decorated(*args, **kwargs):
            # First check token
            token_result = self.token_required(lambda *a, **k: None)()
            if token_result is not None:
                return token_result

            # Check admin role (pseudo-code)
            user = g.get('current_user_id')
            if not self._is_admin(user):
                return jsonify({
                    'error': 'Admin access required',
                    'code': 'AUTH_004'
                }), 403

            return f(*args, **kwargs)

        return decorated

    def _is_admin(self, user_id: int) -> bool:
        """Check if user has admin role"""
        # Implementation would query database
        # For now, assume user 1 is admin
        return user_id == 1


# Example usage with FastAPI would be similar
print("Auth Middleware loaded successfully!")
