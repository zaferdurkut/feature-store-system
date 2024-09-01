from src.core.service.auth.auth_service import AuthService
from src.core.service.offline.offline_service import OfflineService
from src.core.service.stream.stream_service import StreamService
from src.infra.config.dependency_injection_config import get_stream_repository, get_offline_repository


def get_stream_service():
    return StreamService(stream_repository_port=get_stream_repository())

def get_offline_service():
    return OfflineService(offline_repository_port=get_offline_repository())

def get_auth_service():
    return AuthService()
