# Avito API Tests

Автоматизированные API тесты на Python + pytest.

## Установка и запуск

1. Клонировать репозиторий:
```bash
   git clone https://github.com/valeryank/AvitoAPI.git
   cd AvitoAPI
```

2. Создать виртуальное окружение и установить зависимости:
```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
```

3. Запустить тесты:
```bash
   pytest
```

4. Сгенерировать и открыть Allure отчёт:
```bash
   allure serve allure-results
```

## Конфигурация

`pytest.ini` — конфигурация pytest:
- результаты тестов автоматически сохраняются в папку `allure-results`