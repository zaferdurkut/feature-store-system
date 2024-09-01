from typing import cast

from src.core.port.offline_repository_port import OfflineRepositoryPort
from src.core.port.stream_repository_port import StreamRepositoryPort
from src.infra.adapter.repository.redis.offline_cache_adapter import OfflineCacheAdapter
from src.infra.adapter.repository.redis.stream_cache_adapter import StreamCacheAdapter


def get_stream_repository():
    return cast(StreamRepositoryPort, StreamCacheAdapter())


def get_offline_repository():
    return cast(OfflineRepositoryPort, OfflineCacheAdapter())
