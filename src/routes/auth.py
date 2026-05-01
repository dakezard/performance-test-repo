from fastapi import APIRouter
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(username: str, password: str):
    """Login endpoint - returns JWT token"""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(user.id)
    return {"token": token, "user_id": user.id}

@router.post("/logout")
async def logout():
    """Logout endpoint"""
    return {"message": "Logged out successfully"}
