from starlette import status

from src.infra.adapter.repository.redis.repository_config import (
    get_stream_redis_client,
    get_offline_redis_client,
)
from tests.integration.controller.auth.test_constants import AUTH_CONTROLLER_LOGIN_PATH

stream_client = get_stream_redis_client()
offline_client = get_offline_redis_client()


def populate_auth_headers(test_client):
    response = test_client.post(
        AUTH_CONTROLLER_LOGIN_PATH, json={"email": "test@test.com", "password": "test"}
    )
    assert response.status_code == status.HTTP_200_OK

    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def delete_all_repositories():
    stream_client.flushall()
    offline_client.flushall()


def init_repository_data_and_populate_key_and_values() -> dict:

    stream_client.set("avg_review:product_id1", 4.5)
    stream_client.set("last_purchase_amount:customer_id1", 400)
    stream_client.set("last_review:customer_id2_product_id2", 3)
    stream_client.set("revenue_category:category1", 500)
    offline_client.set("avg_review_rating:product_id1", 4.5)
    offline_client.set("revenue_by_category:category2", 2500)
    offline_client.set("revenue_by_product:product_id1", 3500)
    offline_client.set("units_sold:product_id2", 100)

    return {
        "get_product_review_rating_average": {
            "product_id": "product_id1",
            "avg_rating": 4.5,
        },
        "get_customer_last_purchase_amount": {
            "customer_id": "customer_id1",
            "amount": 400,
        },
        "get_customer_last_product_review_rating": {
            "customer_id": "customer_id2",
            "product_id": "product_id2",
            "rating": 3,
        },
        "get_total_revenue_order_by_category": {
            "category": "category1",
            "revenue": 500,
        },
        # offline
        "get_last_month_average_product_review_rating": {
            "product_id": "product_id1",
            "avg_rating": 4.5,
        },
        "get_last_month_category_revenue": {"category": "category2", "revenue": 2500},
        "get_last_month_product_revenue": {
            "product_id": "product_id1",
            "revenue": 3500,
        },
        "get_last_month_sold_product_units": {
            "product_id": "product_id2",
            "units": 100,
        },
    }
