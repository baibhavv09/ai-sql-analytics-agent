from langchain_core.tools import tool
from backend.services.redis_service import redis_service
from backend.services.database_service import database_service
from backend.services.schema_service import SchemaService


@tool
def get_database_schema(user_id: int) -> str:
    """
    Return the user's database schema in an LLM-friendly text format.

    Flow:
    1. Check Redis cache.
    2. If cache miss, extract schema from the user's database.
    3. Cache the schema text.
    4. Return the schema text.
    """

    cache_key = f"schema:{user_id}"

    # Step 1: Check cache
    cached_schema = redis_service.get(cache_key)
    if cached_schema:
        return cached_schema

    # Step 2: Get user's database connection
    connection = database_service.get_connection_by_user_id(user_id)

    if connection is None:
        raise ValueError(f"No database connection found for user {user_id}")

    # Step 3: Create SQLAlchemy engine
    engine = database_service.get_engine_for_user(connection)

    # Step 4: Extract schema
    schema_service = SchemaService(engine)
    schema_text = schema_service.get_schema_prompt()

    # Step 5: Cache schema (1 hour)
    redis_service.set(
        key=cache_key,
        value=schema_text,
        ttl=3600,
    )

    # Step 6: Return schema
    return schema_text


schema_tool = get_database_schema