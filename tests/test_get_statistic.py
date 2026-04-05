import pytest
import requests
import allure
import uuid

BASE_URL = "https://qa-internship.avito.com"


@allure.feature("Получение статистики по объявлению")
class TestGetStatistic:

    @allure.title("TC-04-01 — Получить статистику по существующему объявлению")
    @allure.description("Проверяем что поля статистики совпадают с данными при создании")
    @allure.tag("positive")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_get_statistic_success(self, created_item):
        with allure.step("Отправляем GET запрос с валидным id"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/{created_item['id']}")
        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200
        with allure.step("Проверяем поля статистики"):
            statistic = response.json()[0]
            assert statistic["likes"] == created_item["statistics"]["likes"]
            assert statistic["viewCount"] == created_item["statistics"]["viewCount"]
            assert statistic["contacts"] == created_item["statistics"]["contacts"]

    @allure.title("TC-04-02 — Получить статистику по несуществующему UUID")
    @allure.description("Проверяем что сервер возвращает 404 для несуществующего UUID")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_statistic_not_found(self):
        random_uuid = str(uuid.uuid4())
        with allure.step(f"Отправляем GET запрос с несуществующим UUID: {random_uuid}"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/{random_uuid}")
        with allure.step("Проверяем статус код 404"):
            assert response.status_code == 404
        with allure.step("Проверяем что message содержит переданный id"):
            assert random_uuid in response.json()["result"]["message"]

    @allure.title("TC-04-03 — Передать id в неверном формате")
    @allure.description("Проверяем что сервер возвращает 400 если передать число вместо UUID")
    @allure.tag("negative")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_statistic_invalid_id_format(self):
        with allure.step("Отправляем GET запрос с id=123"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/123")
        with allure.step("Проверяем статус код 400"):
            assert response.status_code == 400
        with allure.step("Проверяем message"):
            assert response.json()["result"]["message"] == "передан некорректный идентификатор объявления"

    @allure.title("TC-04-04 — Пустой id")
    @allure.description("Проверяем поведение сервера при пустом id")
    @allure.tag("corner-case")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_statistic_empty_id(self):
        with allure.step("Отправляем GET запрос с пустым id"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/")
        with allure.step("Проверяем статус код 404"):
            assert response.status_code == 404

    @allure.title("TC-04-05 — Время ответа менее 2 секунд")
    @allure.description("Проверяем что сервер отвечает менее чем за 2000 мс")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_statistic_response_time(self, created_item):
        with allure.step("Отправляем запрос и замеряем время"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/{created_item['id']}")
        with allure.step("Проверяем что ответ пришёл менее чем за 2000 мс"):
            assert response.elapsed.total_seconds() < 2

    @allure.title("TC-04-06 — Content-Type ответа application/json")
    @allure.description("Проверяем что сервер возвращает Content-Type: application/json")
    @allure.tag("non-functional")
    @allure.severity(allure.severity_level.MINOR)
    def test_get_statistic_content_type(self, created_item):
        with allure.step("Отправляем запрос"):
            response = requests.get(f"{BASE_URL}/api/1/statistic/{created_item['id']}")
        with allure.step("Проверяем заголовок Content-Type"):
            assert "application/json" in response.headers["Content-Type"]