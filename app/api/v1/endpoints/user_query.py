from fastapi import APIRouter, Depends
from app.schemas.user_query_schema import UserQueryResponse, UserQueryRequest
from app.services.auth.jwt_setup import get_current_user
from app.services.user_query_service import query


router = APIRouter()

@router.post("/ask", response_model=UserQueryResponse)
def ask(request: UserQueryRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]

    return query(user_id=user_id, query=request.query)
