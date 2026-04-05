import pytest
import requests
import allure
import uuid

BASE_URL = "https://qa-internship.avito.com"


@allure.feature("Получение объявления по ID")
class TestGetItem:

    @allure.title("TC-02-01 — Получить существующее объявление")
    @allure.description("Проверяем что поля ответа совпадают с данными при создании")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_item_success(self, created_item):
        with allure.step("Отправляем GET запрос с валидным id"):
            response = requests.get(f"{BASE_URL}/api/1/item/{created_item['id']}")
        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверяем поля ответа"):
            item = response.json()[0]
            assert item["id"] == created_item["id"]
            assert item["name"] == created_item["name"]
            assert item["price"] == created_item["price"]
            assert item["sellerId"] == created_item["sellerID"]

    @allure.title("TC-02-02 — Получить объявление по несуществующему UUID")
    @allure.description("Проверяем что сервер возвращает 404 для несуществующего UUID")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_item_not_found(self):
        random_uuid = str(uuid.uuid4())
        with allure.step(f"Отправляем GET запрос с несуществующим UUID: {random_uuid}"):
            response = requests.get(f"{BASE_URL}/api/1/item/{random_uuid}")
        with allure.step("Проверяем статус код 404"):
            assert response.status_code == 404
        with allure.step("Проверяем что message содержит переданный id"):
            assert random_uuid in response.json()["result"]["message"]

    @allure.title("TC-02-03 — Передать id в неверном формате")
    @allure.description("Проверяем что сервер возвращает 400 если передать число вместо UUID")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_item_invalid_id_format(self):
        with allure.step("Отправляем GET запрос с id=123"):
            response = requests.get(f"{BASE_URL}/api/1/item/123")
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400
        with allure.step("Проверяем message"):
            assert response.json()["result"]["message"] == "ID айтема не UUID: 123"

    @allure.title("TC-02-04 — Пустой id")
    @allure.description("Проверяем поведение сервера при пустом id")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_item_empty_id(self):
        with allure.step("Отправляем GET запрос с пустым id"):
            response = requests.get(f"{BASE_URL}/api/1/item/")
        with allure.step("Проверяем статус код 404"):
            assert response.status_code == 404


    @allure.title("TC-02-05 — Время ответа менее 2 секунд")
    @allure.description("Проверяем что сервер отвечает менее чем за 2000 мс")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_item_response_time(self, created_item):
        with allure.step("Отправляем GET запрос и замеряем время"):
            response = requests.get(f"{BASE_URL}/api/1/item/{created_item['id']}")
        with allure.step("Проверяем что ответ пришёл менее чем за 2000 мс"):
            assert response.elapsed.total_seconds() < 2

    @allure.title("TC-02-06 — Content-Type ответа application/json")
    @allure.description("Проверяем что сервер возвращает Content-Type: application/json")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_item_content_type(self, created_item):
        with allure.step("Отправляем GET запрос"):
            response = requests.get(f"{BASE_URL}/api/1/item/{created_item['id']}")
        with allure.step("Проверяем заголовок Content-Type"):
            assert "application/json" in response.headers["Content-Type"]