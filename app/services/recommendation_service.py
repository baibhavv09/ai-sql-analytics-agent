import json

from app.ai.llm import llm_service
from app.prompts.recommendation_prompt import recommendation_prompt


class RecommendationService:
    """
    Generates business insights from SQL query results.
    """

    MAX_ROWS = 20

    def generate(self, result: dict) -> dict:
        """
        Generate business recommendations using the LLM.
        """

        if not result.get("success"):
            return {
                "summary": "",
                "recommendations": [],
            }

        sample_result = {
            "columns": result["columns"],
            "rows": result["rows"][: self.MAX_ROWS],
            "row_count": result["row_count"],
        }

        prompt = recommendation_prompt.format(
            result=json.dumps(sample_result, indent=2)
        )

        response = llm_service.invoke(prompt)

        try:
            return json.loads(response.content)

        except Exception:

            return {
                "summary": response.content,
                "recommendations": [],
            }


recommendation_service = RecommendationService()