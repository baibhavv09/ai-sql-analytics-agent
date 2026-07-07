from langchain_core.tools import tool

from backend.services.database_service import database_service
from backend.services.sql_service import SQLService
from backend.services.sql_validator import SQLValidator


@tool
def execute_sql(
    user_id: int,
    sql: str,
) -> dict:
    """
    Execute a validated SQL query on the user's connected database.
    """

    # Step 1: Get database connection
    connection = database_service.get_connection_by_user_id(user_id)

    if connection is None:
        return {
            "success": False,
            "error": "No database connection found for this user."
        }

    # Step 2: Create engine
    engine = database_service.get_engine_for_user(connection)

    # Step 3: Validate SQL
    validation = SQLValidator.validate(sql)

    if not validation["valid"]:
        return {
            "success": False,
            "error": validation["message"]
        }

    # Step 4: Execute SQL
    sql_service = SQLService(engine)

    result = sql_service.execute(sql)

    # History will be added later

    return result


execute_sql_tool = execute_sql