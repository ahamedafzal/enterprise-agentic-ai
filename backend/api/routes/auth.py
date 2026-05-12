from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.core.auth import verify_password, create_access_token, DEMO_USER

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    if request.username != DEMO_USER["username"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(request.password, DEMO_USER["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": request.username})
    return TokenResponse(access_token=token)