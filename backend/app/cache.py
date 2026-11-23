import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple, TypeVar
from sqlalchemy.orm import Session

T = TypeVar("T")


class BindTTLCache:
    """
    Lightweight thread-safe in-memory TTL cache scoped by DB pool identity
    so isolated test databases never share cached entries, while normal and
    AUTOCOMMIT OptionEngine sessions on the same pool share invalidation.
    """

    def __init__(self, ttl_seconds: float):
        self.ttl_seconds = ttl_seconds
        self._lock = threading.Lock()
        self._store: Dict[Tuple[int, str], Tuple[float, Any]] = {}

    @staticmethod
    def _bind_key(db: Session) -> int:
        bind = db.get_bind()
        pool = getattr(bind, "pool", None)
        return id(pool) if pool is not None else id(bind)

    def get_or_set(self, db: Session, key: str, loader: Callable[[], T]) -> T:
        cache_key = (self._bind_key(db), key)
        now = time.monotonic()
        with self._lock:
            entry = self._store.get(cache_key)
            if entry is not None and entry[0] > now:
                return entry[1]

        value = loader()
        with self._lock:
            self._store[cache_key] = (time.monotonic() + self.ttl_seconds, value)
        return value

    def invalidate_all(self, db: Optional[Session] = None) -> None:
        with self._lock:
            if db is None:
                self._store.clear()
                return
            bkey = self._bind_key(db)
            for k in [k for k in self._store if k[0] == bkey]:
                del self._store[k]


departments_cache = BindTTLCache(ttl_seconds=300)
professors_cache = BindTTLCache(ttl_seconds=30)
reviews_cache = BindTTLCache(ttl_seconds=30)
