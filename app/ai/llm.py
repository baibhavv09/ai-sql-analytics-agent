from langchain_openai import ChatOpenAI

from app.core.config import settings


class LLMService:
    """
    Initializes the application's language model.

    This class is responsible only for creating and
    returning a configured ChatOpenAI instance.
    """

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
        )

    def get_llm(self) -> ChatOpenAI:
        """
        Return configured ChatOpenAI instance.
        """

        return self.llm


llm_service = LLMService()