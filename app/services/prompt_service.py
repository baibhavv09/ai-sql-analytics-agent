from typing import Optional

from app.prompts.sql_prompt import SQL_SYSTEM_PROMPT


class PromptService:

    def build_sql_prompt(self,schema: str,question: str,conversation: Optional[str] = None) -> str:

        conversation = conversation or "No previous conversation."

        prompt = f"""
        {SQL_SYSTEM_PROMPT}

        ==============================
        DATABASE SCHEMA
        ==============================

        {schema}

        ==============================
        PREVIOUS CONVERSATION
        ==============================

        {conversation}

        ==============================
        USER QUESTION
        ==============================

        {question}

        ==============================
        OUTPUT
        ==============================

        Generate only SQL.
        """

        return prompt.strip()




prompt_service = PromptService()