import pytest
import requests
import allure

BASE_URL = "https://qa-internship.avito.com"


@allure.feature("Создание объявления")
class TestCreateItem:

    @allure.title("TC-01-01 — Создать объявление со всеми полями")
    @allure.description("Проверяем что объявление создаётся успешно и все поля совпадают с отправленными")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_item_success(self, created_item):
        with allure.step("Проверяем что id не пустой"):
            assert created_item["id"] is not None
        with allure.step("Проверяем поле name"):
            assert created_item["name"] == "Тестовое объявление"
        with allure.step("Проверяем поле price"):
            assert created_item["price"] == 1000
        with allure.step("Проверяем статистику"):
            assert created_item["statistics"]["likes"] == 5
            assert created_item["statistics"]["viewCount"] == 10
            assert created_item["statistics"]["contacts"] == 3

    @allure.title("TC-01-02 — Идемпотентность — два одинаковых объявления получают разные id")
    @allure.description("Создаём два одинаковых объявления и проверяем что они получают разные id")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_idempotency(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем первый запрос"):
            response1 = requests.post(f"{BASE_URL}/api/1/item", json=payload)
            assert response1.status_code == 200
        with allure.step("Отправляем второй запрос с теми же данными"):
            response2 = requests.post(f"{BASE_URL}/api/1/item", json=payload)
            assert response2.status_code == 200
        with allure.step("Проверяем что id разные"):
            id1 = response1.json().get("status", "").split(" - ")[-1]
            id2 = response2.json().get("status", "").split(" - ")[-1]
            assert id1 != id2

        requests.delete(f"{BASE_URL}/api/2/item/{id1}")
        requests.delete(f"{BASE_URL}/api/2/item/{id2}")

    @allure.title("TC-01-03 — Создать объявление без поля name")
    @allure.description("Проверяем что сервер возвращает 400 если не передать поле name")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_without_name(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос без поля name"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-04 — Создать объявление без поля price")
    @allure.description("Проверяем что сервер возвращает 400 если не передать поле price")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_without_price(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос без поля price"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-05 — Создать объявление без поля sellerID")
    @allure.description("Проверяем что сервер возвращает 400 если не передать поле sellerID")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_item_without_seller_id(self):
        payload = {
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос без поля sellerID"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-06 — Отправить пустое тело запроса")
    @allure.description("Проверяем что сервер возвращает 400 при пустом теле запроса")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_empty_body(self):
        with allure.step("Отправляем запрос с пустым телом"):
            response = requests.post(f"{BASE_URL}/api/1/item", json={})
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-07 — Передать price как строку")
    @allure.description("Проверяем что сервер возвращает 400 если передать price как строку")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_price_as_string(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": "тысяча",
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с price как строкой"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-08 — Передать sellerID как строку")
    @allure.description("Проверяем что сервер возвращает 400 если передать sellerID как строку")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_seller_id_as_string(self):
        payload = {
            "sellerID": "abc",
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с sellerID как строкой"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-01-09 — Цена равна нулю")
    @allure.description("Проверяем что сервер принимает price=0. Баг — сервер возвращает 400")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_zero_price(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 0,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с price=0"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 200 (баг — сервер возвращает 400)"):
            assert response.status_code == 200

    @allure.title("TC-01-10 — Отрицательная цена")
    @allure.description("Проверяем что сервер отклоняет отрицательную цену. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_negative_price(self, seller_id):  # ¹
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": -100,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с отрицательной ценой"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-11 — Очень длинное name (1000 символов)")
    @allure.description("Проверяем что сервер отклоняет слишком длинное name. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_item_long_name(self, seller_id):  # ¹
        payload = {
            "sellerID": seller_id,
            "name": "a" * 1000,
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с name из 1000 символов"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-12 — contacts больше viewCount")
    @allure.description("Проверяем бизнес-логику: contacts не может быть больше viewCount. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_item_contacts_more_than_views(self, seller_id):  # ¹
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 1, "contacts": 100}
        }
        with allure.step("Отправляем запрос с contacts > viewCount"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-13 — Отрицательный sellerID")
    @allure.description("Проверяем что сервер отклоняет отрицательный sellerID. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_negative_seller_id(self):  # ¹
        payload = {
            "sellerID": -1,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос с отрицательным sellerID"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-14 — Отрицательный viewCount")
    @allure.description("Проверяем что сервер отклоняет отрицательный viewCount. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_negative_view_count(self, seller_id):  # ¹
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": -1, "contacts": 3}
        }
        with allure.step("Отправляем запрос с отрицательным viewCount"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-15 — Отрицательный contacts")
    @allure.description("Проверяем что сервер отклоняет отрицательный contacts. Баг — сервер возвращает 200")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_negative_contacts(self, seller_id):  # ¹
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": -1}
        }
        with allure.step("Отправляем запрос с отрицательным contacts"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 400 (баг — сервер возвращает 200)"):
            assert response.status_code == 400

    @allure.title("TC-01-16 — Все показатели статистики равны нулю")
    @allure.description("Проверяем что сервер принимает нулевую статистику. Баг — сервер возвращает 400")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_zero_statistics(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 0, "viewCount": 0, "contacts": 0}
        }
        with allure.step("Отправляем запрос с нулевой статистикой"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем статус код 200 (баг — сервер возвращает 400)"):
            assert response.status_code == 200

    @allure.title("TC-01-18 — Время ответа менее 2 секунд")
    @allure.description("Проверяем что сервер отвечает менее чем за 2000 мс")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_item_response_time(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос и замеряем время"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем что ответ пришёл менее чем за 2000 мс"):
            assert response.elapsed.total_seconds() < 2

        item_id = response.json().get("status", "").split(" - ")[-1]
        if item_id:
            requests.delete(f"{BASE_URL}/api/2/item/{item_id}")

    @allure.title("TC-01-19 — Content-Type ответа application/json")
    @allure.description("Проверяем что сервер возвращает Content-Type: application/json")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.MINOR)
    def test_create_item_content_type(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Отправляем запрос"):
            response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
        with allure.step("Проверяем заголовок Content-Type"):
            assert "application/json" in response.headers["Content-Type"]

        item_id = response.json().get("status", "").split(" - ")[-1]
        if item_id:
            requests.delete(f"{BASE_URL}/api/2/item/{item_id}")