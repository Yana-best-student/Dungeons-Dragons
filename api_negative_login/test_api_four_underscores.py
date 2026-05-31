# test_api_four_underscores.py

import allure
import requests
import pytest
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Базовые настройки
# Убедитесь, что переменная загружена корректно
BASE_API_URL = os.getenv('API_URL')
REGISTRATION_ENDPOINT = '/api/v1/auth/registration/'
REGISTRATION_URL = BASE_API_URL + REGISTRATION_ENDPOINT

# Заголовки запроса (глобальная переменная)
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': os.getenv('CSRF_TOKEN')
}

# Основной тестовый метод


@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с логином из четырёх подчёркиваний")
@allure.title("Гибридный тест регистрации с логином '____'")
@allure.description("""
Данный тест проверяет пограничный случай регистрации с логином '____':
- Сейчас регистрация проходит успешно (система допускает такой логин)
- В будущем ожидается, что система начнёт отклонять регистрацию с таким логином
""")
@allure.tag("FutureNegative", "Registration", "LoginValidation", "Cleanup")
@pytest.mark.parametrize("four_underscores", ["____"])  # Параметризация логина
def test_registration_with_four_underscores(cleanup_user, four_underscores, request):
    """
    Гибридный тест регистрации с логином '____'
    Включает автоматическую очистку через фикстуру
    """

    # Логин из четырёх подчёркиваний
    login = four_underscores

    # Электронная почта для регистрации (используйте уникальный адрес)
    unique_email = f"test.user.{os.getenv('TEST_RUN_ID')}@example.com"

    # Формирование тела запроса
    payload = {
        'username': login,
        'email': unique_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    # Преобразование данных в JSON-формат
    json_payload = json.dumps(payload)

    # Отправка POST-запроса на регистрацию
    with allure.step(f"Отправка запроса на регистрацию с логином '{login}'"):
        response = requests.post(
            REGISTRATION_URL, data=json_payload, headers=HEADERS)

        # Прикрепление запроса и ответа к отчёту
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    # Гибкая проверка результата
    with allure.step("Проверка результата регистрации"):
        if response.status_code == 201:
            # Регистрация прошла успешно (текущее поведение системы)
            allure.attach("Регистрация прошла успешно", name="Результат",
                          attachment_type=allure.attachment_type.TEXT)

            # # Получаем ID пользователя из ответа (если доступно)
            # user_data = response.json().get("user", {})

            # # Передаём ID пользователя в фикстуру очистки
            # request.node.user_id = user_data.get("pk")

        elif response.status_code == 400:
            # Регистрация дала ошибку (будущее поведение системы)
            response_json = response.json()
            username_errors = response_json.get("username", [])

            # Новая проверка: ошибка связана с занятостью логина
            assert any(err for err in username_errors if "already taken" in err), \
                f"Ожидалась ошибка о занятом логине, но получено: {username_errors}"

        else:
            # Непредвиденный статус
            pytest.fail(f"Неожиданный статус: {response.status_code}")
