from functools import wraps
from flask import request, jsonify, g

def auth_middleware(f):
    """Authentication middleware to verify JWT tokens"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Missing or invalid authorization header'}), 401
        
        token = auth_header.split(' ')[1]
        
        try:
            # Decode and verify the token
            payload = decode_jwt_token(token)
            g.current_user_id = payload.get('user_id')
            g.user_role = payload.get('role')
            
            return f(*args, **kwargs)
            
        except TokenExpiredError:
            return jsonify({'error': 'Token has expired'}), 401
        except InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
    
    return decorated_function
