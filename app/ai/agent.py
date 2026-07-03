from langchain.agents import AgentExecutor, create_tool_calling_agent

from app.ai.llm import llm_service
from app.prompts.sql_prompt import sql_prompt

# Import tools 
from app.ai.tools.schema_tool import schema_tool
from app.ai.tools.execute_sql_tool import execute_sql_tool
from app.ai.tools.history_tool import history_tool
from app.ai.tools.analytics_tool import analytics_tool


class SQLAnalyticsAgent:

    def __init__(self):

        self.llm = llm_service.get_llm()

        self.tools = [
            schema_tool,
            execute_sql_tool,
            history_tool,
            analytics_tool,
        ]

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
        )

    def invoke(
        self,
        question: str,
        chat_history=None,
    ):

        chat_history = chat_history or []

        return self.executor.invoke(
            {
                "input": question,
                "chat_history": chat_history,
            }
        )


sql_agent = SQLAnalyticsAgent()