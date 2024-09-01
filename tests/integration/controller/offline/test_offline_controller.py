import pytest
from requests import Response
from starlette import status

from tests.integration.controller.offline.test_constants import (
    OFFLINE_REVIEW_RATING_AVERAGE_PATH,
    OFFLINE_CATEGORY_REVENUE_PATH,
    OFFLINE_PRODUCT_REVENUE_PATH,
    OFFLINE_SOLD_PRODUCT_UNITS_PATH,
)
from tests.test_input_common import (
    delete_all_repositories,
    init_repository_data_and_populate_key_and_values,
    populate_auth_headers,
)


@pytest.fixture(autouse=True)
def clear_all_repositories_before_after_each_method():
    delete_all_repositories()
    yield
    delete_all_repositories()


class TestOfflineController:
    def test_should_get_product_review_rating_average(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_product_review_rating_average"
        ]
        product_id = keys_and_values["product_id"]
        avg_rating = keys_and_values["avg_rating"]
        # when
        get_product_review_rating_average_response: Response = test_client.get(
            OFFLINE_REVIEW_RATING_AVERAGE_PATH,
            params={"product_id": product_id},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_product_review_rating_average_response.status_code == status.HTTP_200_OK
        )
        response_data = get_product_review_rating_average_response.json()
        assert response_data["avg_rating"] == avg_rating

    def test_should_raise_not_found_error_when_get_product_review_rating_average_not_found_when_product_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_product_review_rating_average_response: Response = test_client.get(
            OFFLINE_REVIEW_RATING_AVERAGE_PATH,
            params={"product_id": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_product_review_rating_average_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_product_review_rating_average_response.json()
        assert response_data["error_code"] == 2007

    def test_should_raise_bad_request_error_when_get_product_review_rating_average_bad_request_if_product_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_product_review_rating_average_response: Response = test_client.get(
            OFFLINE_REVIEW_RATING_AVERAGE_PATH,
            params={"key": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_product_review_rating_average_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_product_review_rating_average_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_last_month_category_revenue(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_last_month_category_revenue"
        ]
        category = keys_and_values["category"]
        revenue = keys_and_values["revenue"]
        # when
        get_last_month_category_revenue_response: Response = test_client.get(
            OFFLINE_CATEGORY_REVENUE_PATH,
            params={"category": category},
            headers=populate_auth_headers(test_client),
        )

        # then
        get_last_month_category_revenue_response.status_code == status.HTTP_200_OK
        response_data = get_last_month_category_revenue_response.json()
        assert response_data["revenue"] == revenue

    def test_should_raise_not_found_error_when__get_last_month_category_revenue_not_found_if_category_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_last_month_category_revenue_response: Response = test_client.get(
            OFFLINE_CATEGORY_REVENUE_PATH,
            params={"category": "category"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_category_revenue_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_last_month_category_revenue_response.json()
        assert response_data["error_code"] == 2008

    def test_should_raise_bad_request_error_when_get_last_month_category_revenue_bad_request_if_category_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_last_month_category_revenue_response: Response = test_client.get(
            OFFLINE_CATEGORY_REVENUE_PATH,
            params={"key": "category"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_category_revenue_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_last_month_category_revenue_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_last_month_product_revenue(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_last_month_product_revenue"
        ]
        product_id = keys_and_values["product_id"]
        revenue = keys_and_values["revenue"]
        # when
        get_last_month_product_revenue_response: Response = test_client.get(
            OFFLINE_PRODUCT_REVENUE_PATH,
            params={"product_id": product_id},
            headers=populate_auth_headers(test_client),
        )

        # then
        get_last_month_product_revenue_response.status_code == status.HTTP_200_OK
        response_data = get_last_month_product_revenue_response.json()
        assert response_data["revenue"] == revenue

    def test_should_raise_not_found_error_when_get_last_month_product_revenue_not_found_if_product_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_last_month_product_revenue_response: Response = test_client.get(
            OFFLINE_PRODUCT_REVENUE_PATH,
            params={"product_id": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_product_revenue_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_last_month_product_revenue_response.json()
        assert response_data["error_code"] == 2009

    def test_should_raise_bad_request_error_when_get_last_month_product_revenue_bad_request_if_product_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_last_month_product_revenue_response: Response = test_client.get(
            OFFLINE_PRODUCT_REVENUE_PATH,
            params={"key": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_product_revenue_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_last_month_product_revenue_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_last_month_sold_product_units(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_last_month_sold_product_units"
        ]
        product_id = keys_and_values["product_id"]
        units = keys_and_values["units"]
        # when
        get_last_month_sold_product_units_response: Response = test_client.get(
            OFFLINE_SOLD_PRODUCT_UNITS_PATH,
            params={"product_id": product_id},
            headers=populate_auth_headers(test_client),
        )

        # then
        get_last_month_sold_product_units_response.status_code == status.HTTP_200_OK
        response_data = get_last_month_sold_product_units_response.json()
        assert response_data["units"] == units

    def test_should_raise_not_found_error_when_get_last_month_sold_product_units_not_found_if_product_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_last_month_sold_product_units_response: Response = test_client.get(
            OFFLINE_SOLD_PRODUCT_UNITS_PATH,
            params={"product_id": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_sold_product_units_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_last_month_sold_product_units_response.json()
        assert response_data["error_code"] == 2010

    def test_should_raise_bad_request_error_when_get_last_month_sold_product_units_bad_request_if_product_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_last_month_sold_product_units_response: Response = test_client.get(
            OFFLINE_SOLD_PRODUCT_UNITS_PATH,
            params={"key": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_last_month_sold_product_units_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_last_month_sold_product_units_response.json()
        assert response_data["error_code"] == 1000
