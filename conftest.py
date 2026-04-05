import pytest
import requests
import random

BASE_URL = "https://qa-internship.avito.com"


def generate_seller_id():
    return random.randint(111111, 999999)


@pytest.fixture
def seller_id():
    return generate_seller_id()


@pytest.fixture
def created_item(seller_id):
    # SETUP — создаём объявление перед тестом
    payload = {
        "sellerID": seller_id,
        "name": "Тестовое объявление",
        "price": 1000,
        "statistics": {
            "likes": 5,
            "viewCount": 10,
            "contacts": 3
        }
    }
    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    item = response.json()

    # достаём id из строки "Сохранили объявление - 17aa3f02-..."
    item_id = item.get("status", "").split(" - ")[-1]

    yield {"id": item_id, **payload}  # передаём id + данные которые отправляли

    # TEARDOWN
    if item_id:
        requests.delete(f"{BASE_URL}/api/2/item/{item_id}")