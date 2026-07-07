import time

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class SQLService:
    """
    Service responsible for executing validated SQL queries.
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def execute(self, sql: str) -> dict:
        """
        Execute a validated SQL query.

        Returns:
        {
            "success": bool,
            "columns": [],
            "rows": [],
            "row_count": int,
            "execution_time_ms": float,
            "error": str | None
        }
        """

        start_time = time.perf_counter()

        try:
            with self.engine.connect() as connection:

                result = connection.execute(text(sql))

                rows = result.fetchall()

                columns = list(result.keys())

                execution_time = (
                    time.perf_counter() - start_time
                ) * 1000

                return {
                    "success": True,
                    "columns": columns,
                    "rows": [list(row) for row in rows],
                    "row_count": len(rows),
                    "execution_time_ms": round(execution_time, 2),
                }

        except SQLAlchemyError as e:

            execution_time = (
                time.perf_counter() - start_time
            ) * 1000

            return {
                "success": False,
                "error": str(e),
                "columns": [],
                "rows": [],
                "row_count": 0,
                "execution_time_ms": round(execution_time, 2),
            }