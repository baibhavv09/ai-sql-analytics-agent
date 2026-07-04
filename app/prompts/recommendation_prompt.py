from langchain_core.prompts import PromptTemplate

recommendation_prompt = PromptTemplate.from_template(
"""
You are a senior business analyst.

Analyze the SQL query result below.

Return ONLY valid JSON.

Format:

{{
    "summary":"Short summary in 2-3 sentences.",
    "recommendations":[
        "...",
        "...",
        "..."
    ]
}}

SQL Result:

{result}
"""
)