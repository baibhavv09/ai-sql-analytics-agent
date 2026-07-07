import json
import logging
from typing import Any, Optional

import redis
from redis.exceptions import RedisError

from backend.core.config import settings

logger = logging.getLogger(__name__)


class RedisService:
    """
    Generic Redis Service.

    Used for:
    - Schema Cache
    - Conversation Memory
    - LLM Cache
    - Session Cache
    """

    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )


    def ping(self) -> bool:
        """
        Check Redis connection.
        """

        try:
            return self.client.ping()

        except RedisError as e:
            logger.error(f"Redis Ping Error: {e}")
            return False


    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Store any JSON serializable object.
        """

        try:

            data = json.dumps(value)

            self.client.set(
                key,
                data,
                ex=ttl,
            )

            return True

        except Exception as e:
            logger.error(f"Redis SET Error: {e}")
            return False

  

    def get(
        self,
        key: str,
    ) -> Any:
        """
        Retrieve cached object.
        """

        try:

            data = self.client.get(key)

            if data is None:
                return None

            return json.loads(data)

        except Exception as e:
            logger.error(f"Redis GET Error: {e}")
            return None

   

    def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete a cache key.
        """

        try:

            self.client.delete(key)

            return True

        except Exception as e:
            logger.error(f"Redis DELETE Error: {e}")
            return False

 

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether key exists.
        """

        try:

            return self.client.exists(key) > 0

        except Exception as e:
            logger.error(f"Redis EXISTS Error: {e}")
            return False

  

    def expire(
        self,
        key: str,
        ttl: int,
    ) -> bool:
        """
        Update key expiration.
        """

        try:

            self.client.expire(
                key,
                ttl,
            )

            return True

        except Exception as e:
            logger.error(f"Redis EXPIRE Error: {e}")
            return False



    def ttl(
        self,
        key: str,
    ) -> int:
        """
        Get remaining TTL.
        """

        try:

            return self.client.ttl(key)

        except Exception as e:
            logger.error(f"Redis TTL Error: {e}")
            return -1

    

    def increment(
        self,
        key: str,
        amount: int = 1,
    ) -> int:
        """
        Increment numeric value.
        """

        try:

            return self.client.incr(
                key,
                amount,
            )

        except Exception as e:
            logger.error(f"Redis Increment Error: {e}")
            return 0

    

    def keys(
        self,
        pattern: str = "*",
    ) -> list[str]:
        """
        Return keys matching pattern.
        """

        try:

            return self.client.keys(pattern)

        except Exception as e:
            logger.error(f"Redis KEYS Error: {e}")
            return []

  

    def clear(self) -> bool:
        """
        Flush current Redis database.
        """

        try:

            self.client.flushdb()

            return True

        except Exception as e:
            logger.error(f"Redis CLEAR Error: {e}")
            return False

  

    def hset(
        self,
        key: str,
        mapping: dict,
    ) -> bool:
        """
        Store Redis Hash.
        """

        try:

            self.client.hset(
                key,
                mapping={
                    k: json.dumps(v)
                    for k, v in mapping.items()
                },
            )

            return True

        except Exception as e:
            logger.error(f"Redis HSET Error: {e}")
            return False

  

    def hgetall(
        self,
        key: str,
    ) -> dict:
        """
        Retrieve Redis Hash.
        """

        try:

            result = self.client.hgetall(key)

            return {
                k: json.loads(v)
                for k, v in result.items()
            }

        except Exception as e:
            logger.error(f"Redis HGETALL Error: {e}")
            return {}

  

    def close(self):
        """
        Close Redis connection.
        """

        try:

            self.client.close()

        except Exception:
            pass


redis_service = RedisService()