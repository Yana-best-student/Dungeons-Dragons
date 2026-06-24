import allure
import requests
import json
import os
import pytest
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Базовый URL проекта
BASE_API_URL = os.getenv('API_URL')
if not BASE_API_URL:
    raise ValueError("Переменная окружения API_URL не установлена.")

# Эндпоинт регистрации
REGISTRATION_URL = f"{BASE_API_URL}/api/v1/auth/registration/"
HEADERS = {'accept': 'application/json'}

@pytest.mark.xfail(reason='Бэк не валидирует максимальную длину email. Ожидаемый статус 400.')
@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с недопустимой почтой")
@allure.title("Регистрация с email длиной 255 символов")
@allure.description(
    """
    Тест проверяет реакцию системы на попытку регистрации с email, превышающим максимальный размер.
    Ожидается отказ регистрации с соответствующим сообщением об ошибке.
    """
)
@allure.tag("Negative", "EmailValidation", "Registration")
def test_too_long_email():
    """
    Негативный тест регистрации с недопустимым email (слишком длинной строкой).
    Ожидается отказ регистрации с сообщением об ошибке.
    """

    # Создаем строку длиной 255 символов
    local_part = "a" * 255
    domain = "@example.com"
    invalid_email = local_part + domain

    payload = {
        "username": "scorpio",
        "email": invalid_email,
        "password1": "SecurePass123!",
        "password2": "SecurePass123!",
        "light_theme": False,
        "dark_theme": True,
    }

    with allure.step(f"Отправка запроса на регистрацию с email '{invalid_email[:50]}...'"):
        response = requests.post(
            REGISTRATION_URL, json=payload, headers=HEADERS
        )

        allure.attach(
            json.dumps(payload, indent=2),
            name="Запрос",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            str(response.text),
            name="Ответ",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Проверка ответа сервера"):
        assert response.status_code == 400, f"Прилетел статус {response.status_code}, а ожидался 400"

        errors = response.json()

        # Проверка, что ошибка пришла именно по полю email
        assert "email" in errors, "В ответе нет сообщения об ошибке в поле email"
        assert isinstance(errors["email"], list), "Ошибка должна быть списком"
        assert len(errors["email"]) >= 1, "Нет текста ошибки"