import pytest
from starlette.testclient import TestClient

from main import app
from src.core.service.offline.offline_service import OfflineService
from src.core.service.stream.stream_service import StreamService
from src.infra.adapter.repository.redis.offline_cache_adapter import OfflineCacheAdapter
from src.infra.adapter.repository.redis.stream_cache_adapter import StreamCacheAdapter


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app, base_url="http://localhost")


@pytest.fixture(scope="session")
def stream_repository_adapter():
    return StreamCacheAdapter()


@pytest.fixture(scope="session")
def offline_repository_adapter():
    return OfflineCacheAdapter()


@pytest.fixture(scope="session")
def stream_service(
    stream_repository_adapter,
):
    return StreamService(stream_repository_port=stream_repository_adapter)


@pytest.fixture(scope="session")
def offline_service(
    offline_repository_adapter,
):
    return OfflineService(offline_repository_port=offline_repository_adapter)
