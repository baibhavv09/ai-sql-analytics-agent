from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SQL_SYSTEM_PROMPT = """
You are an expert SQL Engineer.

Generate only safe SQL.

Never generate:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE

Use available tools whenever you need schema information or query execution.
"""


sql_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SQL_SYSTEM_PROMPT),

        MessagesPlaceholder("chat_history"),

        ("human", "{input}"),

        MessagesPlaceholder("agent_scratchpad"),
    ]
)