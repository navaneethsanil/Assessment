from fastapi import APIRouter
from app.schemas.auth_schema import LoginResponse, LoginRequest
from app.services.auth import auth_service


router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    return auth_service.login(email=request.email, password=request.password)