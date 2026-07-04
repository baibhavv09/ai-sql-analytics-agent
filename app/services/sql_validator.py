import re


class SQLValidator:
    """
    Validates AI-generated SQL before execution.
    Only read-only queries are allowed.
    """

    ALLOWED_COMMANDS = {
        "SELECT",
        "WITH",
        "SHOW",
        "DESCRIBE",
        "DESC",
        "EXPLAIN",
        "WHERE",
        "GROUP",
        "ORDER",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "FULL",
        "CROSS",
        "UNION",
        "INTERSECT",
        "EXCEPT",
        "AS",
        "ON",
        "IN",
        "IS",
        "NULL",
    }

    BLOCKED_COMMANDS = {
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE",
        "MERGE",
        "CALL",
        "EXEC",
        "EXECUTE",
        "GRANT",
        "REVOKE",
        "COMMIT",
        "ROLLBACK",
        "SET",
        "USE",
    }

    @classmethod
    def validate(cls, sql: str) -> dict:
        """
        Validate an SQL query before execution.
        """

        if not sql or not sql.strip():
            return {
                "valid": False,
                "message": "SQL query cannot be empty.",
            }

        sql = sql.strip()

        # Prevent multiple statements
        if ";" in sql.rstrip(";"):
            return {
                "valid": False,
                "message": "Multiple SQL statements are not allowed.",
            }

        sql_upper = sql.upper()

        # Block dangerous commands anywhere in the query
        for command in cls.BLOCKED_COMMANDS:
            if re.search(rf"\b{command}\b", sql_upper):
                return {
                    "valid": False,
                    "message": f"{command} statements are not allowed.",
                }

        # Check first command
        first_word = sql_upper.split()[0]

        if first_word not in cls.ALLOWED_COMMANDS:
            return {
                "valid": False,
                "message": f"{first_word} is not an allowed SQL command.",
            }

        return {
            "valid": True,
            "message": "SQL validation successful.",
        }