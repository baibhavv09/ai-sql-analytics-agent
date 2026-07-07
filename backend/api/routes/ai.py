from fastapi import APIRouter, Depends

from backend.ai.agent import sql_agent
from backend.schemas.ai import AIQueryRequest
from backend.api.dependencies.auth import get_current_user
from backend.db.models import User

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/query")
def query_ai(
    request: AIQueryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ask questions in natural language.
    """

    response = sql_agent.invoke(
        question=request.question,
        user_id=current_user.id      # Add this later
    )

    return response