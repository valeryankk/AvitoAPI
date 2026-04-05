import pytest
import requests
import allure
import uuid

BASE_URL = "https://qa-internship.avito.com"


@allure.feature("Получение объявлений продавца")
class TestGetSellerItems:

    @allure.title("TC-03-01 — Получить объявления продавца с несколькими объявлениями")
    @allure.description("Проверяем что возвращается массив объявлений и все принадлежат этому продавцу")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_seller_items_multiple(self, seller_id):
        payload = {
            "sellerID": seller_id,
            "name": "Тестовое объявление",
            "price": 1000,
            "statistics": {"likes": 5, "viewCount": 10, "contacts": 3}
        }
        with allure.step("Создаём два объявления"):
            response1 = requests.post(f"{BASE_URL}/api/1/item", json=payload)
            response2 = requests.post(f"{BASE_URL}/api/1/item", json=payload)
            id1 = response1.json().get("status", "").split(" - ")[-1]
            id2 = response2.json().get("status", "").split(" - ")[-1]

        with allure.step("Получаем все объявления продавца"):
            response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверяем что вернулся массив из 2+ элементов"):
            items = response.json()
            assert len(items) >= 2
        with allure.step("Проверяем что все объявления принадлежат этому продавцу"):
            for item in items:
                assert item["sellerId"] == seller_id

        requests.delete(f"{BASE_URL}/api/2/item/{id1}")
        requests.delete(f"{BASE_URL}/api/2/item/{id2}")

    @allure.title("TC-03-02 — Получить объявления продавца с одним объявлением")
    @allure.description("Проверяем что возвращается массив из одного элемента")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_seller_items_single(self, created_item):
        with allure.step("Получаем объявления продавца"):
            response = requests.get(f"{BASE_URL}/api/1/{created_item['sellerID']}/item")
        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверяем что вернулся массив из одного элемента"):
            items = response.json()
            assert len(items) == 1
        with allure.step("Проверяем что объявление принадлежит этому продавцу"):
            assert items[0]["sellerId"] == created_item["sellerID"]

    @allure.title("TC-03-04 — sellerID как строка")
    @allure.description("Проверяем что сервер возвращает 400 если передать sellerID как строку")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_seller_items_invalid_seller_id(self):
        with allure.step("Отправляем запрос с sellerID как строкой"):
            response = requests.get(f"{BASE_URL}/api/1/abc/item")
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400
        with allure.step("Проверяем message"):
            assert response.json()["result"]["message"] == "передан некорректный идентификатор продавца"

    @allure.title("TC-03-05 — Продавец без объявлений")
    @allure.description("Проверяем что сервер возвращает пустой массив для продавца без объявлений")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_seller_items_empty(self, seller_id):
        with allure.step("Получаем объявления продавца у которого нет объявлений"):
            response = requests.get(f"{BASE_URL}/api/1/{seller_id}/item")
        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверяем что вернулся пустой массив"):
            assert response.json() == []

    @allure.title("TC-03-06 — Отрицательный sellerID")
    @allure.description("Проверяем что сервер возвращает 400 для отрицательного sellerID")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_seller_items_negative_seller_id(self):
        with allure.step("Отправляем запрос с отрицательным sellerID"):
            response = requests.get(f"{BASE_URL}/api/1/-1/item")
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400

    @allure.title("TC-03-07 — Время ответа менее 2 секунд")
    @allure.description("Проверяем что сервер отвечает менее чем за 2000 мс")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_seller_items_response_time(self, created_item):
        with allure.step("Отправляем запрос и замеряем время"):
            response = requests.get(f"{BASE_URL}/api/1/{created_item['sellerID']}/item")
        with allure.step("Проверяем что ответ пришёл менее чем за 2000 мс"):
            assert response.elapsed.total_seconds() < 2

    @allure.title("TC-03-08 — Content-Type ответа application/json")
    @allure.description("Проверяем что сервер возвращает Content-Type: application/json")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_seller_items_content_type(self, created_item):
        with allure.step("Отправляем запрос"):
            response = requests.get(f"{BASE_URL}/api/1/{created_item['sellerID']}/item")
        with allure.step("Проверяем заголовок Content-Type"):
            assert "application/json" in response.headers["Content-Type"]