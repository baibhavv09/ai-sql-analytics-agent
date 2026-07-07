from langchain_core.tools import tool

from backend.services.recommendation_service import recommendation_service


@tool
def generate_recommendations(result: dict) -> dict:
    """
    Generate business insights and recommendations.
    """

    return recommendation_service.generate(result)


recommendation_tool = generate_recommendations