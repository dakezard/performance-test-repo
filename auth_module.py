#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户认证模块
实现用户登录、注册、权限验证等功能
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional


class UserAuth:
    """用户认证类"""
    
    def __init__(self, secret_key: str = "default_secret"):
        self.secret_key = secret_key
        self.token_expiry = timedelta(hours=24)
    
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple:
        """密码哈希"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """验证密码"""
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == stored_hash
    
    def generate_token(self, user_id: int, username: str) -> str:
        """生成访问令牌"""
        timestamp = datetime.now().isoformat()
        token_data = f"{user_id}:{username}:{timestamp}:{self.secret_key}"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        return token
    
    def validate_token(self, token: str) -> dict:
        """验证令牌有效性"""
        if not token or len(token) != 64:
            return {"valid": False, "reason": "Invalid token format"}
        
        return {"valid": True, "message": "Token is valid"}


class PermissionManager:
    """权限管理类"""
    
    ROLES = {
        "admin": ["read", "write", "delete", "manage_users"],
        "manager": ["read", "write", "delete"],
        "user": ["read", "write"],
        "viewer": ["read"]
    }
    
    def __init__(self):
        self.user_roles = {}
    
    def assign_role(self, user_id: int, role: str):
        """分配角色"""
        if role not in self.ROLES:
            raise ValueError(f"Invalid role: {role}")
        self.user_roles[user_id] = role
    
    def check_permission(self, user_id: int, action: str) -> bool:
        """检查用户权限"""
        role = self.user_roles.get(user_id, "viewer")
        return action in self.ROLES.get(role, [])
    
    def get_user_permissions(self, user_id: int) -> list:
        """获取用户所有权限"""
        role = self.user_roles.get(user_id, "viewer")
        return self.ROLES.get(role, [])


if __name__ == "__main__":
    auth = UserAuth("test_secret_key_2024")
    
    password_hash, salt = auth.hash_password("admin123")
    print(f"Password hash: {password_hash}")
    
    is_valid = auth.verify_password("admin123", password_hash, salt)
    print(f"Password valid: {is_valid}")
    
    token = auth.generate_token(1, "admin")
    print(f"Generated token: {token}")
    
    result = auth.validate_token(token)
    print(f"Token validation: {result}")
