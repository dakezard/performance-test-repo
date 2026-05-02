# login.py - User Authentication Module

import hashlib
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g

SECRET_KEY = "your-secret-key-here"

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify password against hashed value"""
    return hashlib.sha256(password.encode()).hexdigest() == hashed

def generate_token(user_id, username):
    """Generate JWT token for authenticated user"""
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        
        token = token.split(" ")[1] if len(token.split(" ")) > 1 else token
        decoded = decode_token(token)
        
        if not decoded:
            return jsonify({"error": "Token is invalid or expired"}), 401
        
        g.current_user = decoded
        return f(*args, **kwargs)
    
    return decorated_function

def authenticate_user(username, password, db_session):
    """Authenticate user credentials against database"""
    from models import User
    
    user = db_session.query(User).filter(User.username == username).first()
    if not user:
        return None, "User not found"
    
    if not verify_password(password, user.password_hash):
        return None, "Invalid password"
    
    if not user.is_active:
        return None, "User account is disabled"
    
    token = generate_token(user.id, user.username)
    return {"token": token, "user_id": user.id}, None
