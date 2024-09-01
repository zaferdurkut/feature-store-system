import pytest
from requests import Response
from starlette import status

from tests.integration.controller.stream.test_constants import (
    STREAM_REVIEW_RATING_AVERAGE_PATH,
    STREAM_LAST_PURCHASE_AMOUNT_PATH,
    STREAM_LAST_CUSTOMER_PRODUCT_REVIEW_PATH,
    STREAM_TOTAL_REVENUE_BY_CATEGORY_PATH,
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


class TestStreamController:
    def test_should_get_last_month_average_product_review_rating(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_last_month_average_product_review_rating"
        ]
        product_id = keys_and_values["product_id"]
        avg_rating = keys_and_values["avg_rating"]
        # when
        get_last_month_average_product_review_rating_response: Response = (
            test_client.get(
                STREAM_REVIEW_RATING_AVERAGE_PATH,
                params={"product_id": product_id},
                headers=populate_auth_headers(test_client),
            )
        )

        # then
        assert (
            get_last_month_average_product_review_rating_response.status_code
            == status.HTTP_200_OK
        )
        response_data = get_last_month_average_product_review_rating_response.json()
        assert response_data["avg_rating"] == avg_rating

    def test_should_raise_not_found_error_when_get_last_month_average_product_review_rating_if_product_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_last_month_average_product_review_rating_response: Response = (
            test_client.get(
                STREAM_REVIEW_RATING_AVERAGE_PATH,
                params={"product_id": "product_id"},
                headers=populate_auth_headers(test_client),
            )
        )

        # then
        assert (
            get_last_month_average_product_review_rating_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_last_month_average_product_review_rating_response.json()
        assert response_data["error_code"] == 2003

    def test_should_raise_bad_request_error_when_get_last_month_average_product_review_rating_if_product_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_last_month_average_product_review_rating_response: Response = (
            test_client.get(
                STREAM_REVIEW_RATING_AVERAGE_PATH,
                params={"key": "product_id"},
                headers=populate_auth_headers(test_client),
            )
        )

        # then
        assert (
            get_last_month_average_product_review_rating_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_last_month_average_product_review_rating_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_customer_last_purchase_amount(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_customer_last_purchase_amount"
        ]
        customer_id = keys_and_values["customer_id"]
        amount = keys_and_values["amount"]
        # when
        get_customer_last_purchase_amount_response: Response = test_client.get(
            STREAM_LAST_PURCHASE_AMOUNT_PATH,
            params={"customer_id": customer_id},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_purchase_amount_response.status_code == status.HTTP_200_OK
        )
        response_data = get_customer_last_purchase_amount_response.json()
        assert response_data["amount"] == amount

    def test_should_raise_not_found_error_when_get_customer_last_purchase_amount_if_customer_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_customer_last_purchase_amount_response: Response = test_client.get(
            STREAM_LAST_PURCHASE_AMOUNT_PATH,
            params={"customer_id": "customer_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_purchase_amount_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_customer_last_purchase_amount_response.json()
        assert response_data["error_code"] == 2004

    def test_should_raise_bad_request_error_when_get_customer_last_purchase_amount_if_customer_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_customer_last_purchase_amount_response: Response = test_client.get(
            STREAM_LAST_PURCHASE_AMOUNT_PATH,
            params={"key": "customer_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_purchase_amount_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_customer_last_purchase_amount_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_customer_last_product_review_rating(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_customer_last_product_review_rating"
        ]
        customer_id = keys_and_values["customer_id"]
        product_id = keys_and_values["product_id"]
        rating = keys_and_values["rating"]
        # when
        get_customer_last_product_review_rating_response: Response = test_client.get(
            STREAM_LAST_CUSTOMER_PRODUCT_REVIEW_PATH,
            params={"customer_id": customer_id, "product_id": product_id},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_product_review_rating_response.status_code
            == status.HTTP_200_OK
        )
        response_data = get_customer_last_product_review_rating_response.json()
        assert response_data["rating"] == rating

    def test_should_raise_not_found_error_when_get_customer_last_product_review_rating_if_customer_id_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_customer_last_product_review_rating_response: Response = test_client.get(
            STREAM_LAST_CUSTOMER_PRODUCT_REVIEW_PATH,
            params={"customer_id": "customer_id", "product_id": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_product_review_rating_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_customer_last_product_review_rating_response.json()
        assert response_data["error_code"] == 2005

    def test_should_raise_bad_request_error_when_get_customer_last_product_review_rating_if_customer_id_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_customer_last_product_review_rating_response: Response = test_client.get(
            STREAM_LAST_CUSTOMER_PRODUCT_REVIEW_PATH,
            params={"key": "customer_id", "product_id": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_product_review_rating_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_customer_last_product_review_rating_response.json()
        assert response_data["error_code"] == 1000

        # when
        get_customer_last_product_review_rating_response: Response = test_client.get(
            STREAM_LAST_CUSTOMER_PRODUCT_REVIEW_PATH,
            params={"customer_id": "customer_id", "key": "product_id"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_customer_last_product_review_rating_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_customer_last_product_review_rating_response.json()
        assert response_data["error_code"] == 1000

    def test_should_get_total_revenue_order_by_category(self, test_client):
        # given
        keys_and_values: dict = init_repository_data_and_populate_key_and_values()[
            "get_total_revenue_order_by_category"
        ]
        category = keys_and_values["category"]
        revenue = keys_and_values["revenue"]
        # when
        get_total_revenue_order_by_category_response: Response = test_client.get(
            STREAM_TOTAL_REVENUE_BY_CATEGORY_PATH,
            params={"category": category},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_total_revenue_order_by_category_response.status_code
            == status.HTTP_200_OK
        )
        response_data = get_total_revenue_order_by_category_response.json()
        assert response_data["revenue"] == revenue

    def test_should_raise_not_found_error_when_get_total_revenue_order_by_category_if_category_does_not_exist(
        self, test_client
    ):
        # given
        # when
        get_total_revenue_order_by_category_response: Response = test_client.get(
            STREAM_TOTAL_REVENUE_BY_CATEGORY_PATH,
            params={"category": "category"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_total_revenue_order_by_category_response.status_code
            == status.HTTP_404_NOT_FOUND
        )
        response_data = get_total_revenue_order_by_category_response.json()
        assert response_data["error_code"] == 2006

    def test_should_raise_bad_request_error_when_get_total_revenue_order_by_category_if_category_is_invalid(
        self, test_client
    ):
        # given
        # when
        get_total_revenue_order_by_category_response: Response = test_client.get(
            STREAM_TOTAL_REVENUE_BY_CATEGORY_PATH,
            params={"key": "category"},
            headers=populate_auth_headers(test_client),
        )

        # then
        assert (
            get_total_revenue_order_by_category_response.status_code
            == status.HTTP_400_BAD_REQUEST
        )
        response_data = get_total_revenue_order_by_category_response.json()
        assert response_data["error_code"] == 1000
