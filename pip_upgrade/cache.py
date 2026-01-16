import json
import hashlib
import sys

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisCache:
    """Redis cache helper with silent fallback on connection failures."""

    DEFAULT_TTL = 60 * 15  # 15 minutes

    def __init__(self, host="localhost", port=6379, db=0):
        self.client = None
        self.connected = False

        if not REDIS_AVAILABLE:
            return

        try:
            self.client = redis.Redis(host=host, port=port, db=db)
            self.client.ping()
            self.connected = True
        except (redis.ConnectionError, redis.TimeoutError):
            self.client = None
            self.connected = False

    def _make_key(self, key: str) -> str:
        """Create a namespaced cache key."""
        return f"pip-upgrade:{key}"

    def get(self, key: str):
        """Get value from cache. Returns None if not found or on error."""
        if not self.connected:
            return None

        try:
            value = self.client.get(self._make_key(key))
            if value is not None:
                return json.loads(value)
        except (redis.RedisError, json.JSONDecodeError):
            pass
        return None

    def set(self, key: str, value, ttl: int = None):
        """Set value in cache. Silently fails on error."""
        if not self.connected:
            return

        if ttl is None:
            ttl = self.DEFAULT_TTL

        try:
            self.client.setex(
                self._make_key(key),
                ttl,
                json.dumps(value)
            )
        except (redis.RedisError, TypeError):
            pass


def get_env_hash() -> str:
    """Generate a hash based on the Python executable path for cache key uniqueness."""
    return hashlib.md5(sys.executable.encode()).hexdigest()[:8]
