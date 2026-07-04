from langchain_core.tools import tool

from app.services.chart_service import chart_service


@tool
def recommend_chart(result: dict) -> dict:
    """
    Recommend the most suitable chart for SQL query results.
    """
    return chart_service.recommend_chart(result)