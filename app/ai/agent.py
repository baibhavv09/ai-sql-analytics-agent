from langchain.agents import AgentExecutor, create_tool_calling_agent

from app.ai.llm import llm_service
from app.prompts.sql_prompt import sql_prompt

# Import tools 
from app.ai.tools.schema_tool import schema_tool
from app.ai.tools.execute_sql_tool import execute_sql_tool
from app.ai.tools.chart_tool import chart_tool
from app.ai.tools.recommendation_tool import recommendation_tool


class SQLAnalyticsAgent:

    def __init__(self):

        self.tools = [
            schema_tool,
            execute_sql_tool,
            chart_tool,
            recommendation_tool,
        ]

        self.llm = llm_service.get_llm(self.tools)

        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=sql_prompt,
        )

        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="generate",
        )

    def invoke(
        self,
        question: str,
        user_id: int,
    ):

        try:
            return self.executor.invoke(
                {
                    "input": question,
                    "user_id": user_id,
                }
            )

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
        

