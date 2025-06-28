from fastapi import FastAPI
from app.api.v1.endpoints import user, user_query
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Assessment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1", tags=["User"])
app.include_router(user_query.router, prefix="/api/v1", tags=["UserQuery"])