from langchain_openai import ChatOpenAI

from backend.core.config import settings


class LLMService:
    """
    Creates and returns configured ChatOpenAI instances.
    """

    def __init__(self):

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS,
            timeout=60,
            max_retries=3,
        )

    def get_llm(self, tools=None):
        """
        Return configured LLM.

        If tools are provided, return an LLM with tool calling enabled.
        """

        if tools:
            return self.llm.bind_tools(tools)

        return self.llm

    def invoke(self, prompt):
        return self.llm.invoke(prompt)


llm_service = LLMService()