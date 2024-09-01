from requests import Response
from starlette import status

from tests.integration.controller.auth.test_constants import AUTH_CONTROLLER_LOGIN_PATH


class TestAuthController:
    def test_should_login(self, test_client):
        # given
        body = {"email": "fake@example.com", "password": "password"}
        # when
        response: Response = test_client.post(AUTH_CONTROLLER_LOGIN_PATH, json=body)

        # then
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["access_token"] is not None
        assert response_data["refresh_token"] is not None
