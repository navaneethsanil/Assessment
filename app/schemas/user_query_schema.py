from pydantic import BaseModel


class UserQueryRequest(BaseModel):
    query: str


class UserQueryResponse(BaseModel):
    ai_response: str