from fastapi import FastAPI
from sqlalchemy import text
from backend.core.config import settings
from backend.db.database import engine
from backend.db import models
from backend.api.routes.auth import router as auth_router
from backend.api.routes.database import router as database_router
from backend.api.routes.ai import router as ai_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)



app.include_router(ai_router)
app.include_router(auth_router)
app.include_router(database_router)

@app.get("/")
def root():
    return {
        "message": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/health")
def health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
        }
