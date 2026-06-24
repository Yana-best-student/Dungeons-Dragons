import allure
import requests
import json
import os
from dotenv import load_dotenv
import pytest

load_dotenv()

BASE_API_URL = os.getenv('API_URL')
registration_url = BASE_API_URL + '/api/v1/auth/registration/'

HEADERS = {'accept': 'application/json', 'Content-Type': 'application/json'}


@allure.epic("Dungeons & Dragons")
@allure.severity(allure.severity_level.NORMAL)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Регистрация с коротким паролем")
@allure.title("Ошибка при создании пользователя с паролем из 7 символов")
@allure.description(
    "Минимальная длина пароля — 8 символов. Этот тест проверяет, что регистрация с меньшим количеством символов невозможна."
)
def test_short_password_error():
    """Тест проверяет, что система отклоняет короткие пароли."""

    unique_part = os.urandom(4).hex()
    username = f"test_user_{unique_part}"
    email = f"test_email_{unique_part}@example.com"

    short_password = "ShorT1!"  # 7 символов

    payload = {
        "username": username,
        "email": email,
        "password1": short_password,
        "password2": short_password,
        "light_theme": False,
        "dark_theme": True,
    }

    with allure.step("Отправка запроса на регистрацию"):
        response = requests.post(
            registration_url, data=json.dumps(payload), headers=HEADERS
        )

        allure.attach(
            json.dumps(payload, indent=2),
            name="Запрос",
            attachment_type=allure.attachment_type.JSON,
        )
        allure.attach(
            str(response.text),
            name="Ответ",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 400, f"Прилетел статус {response.status_code}, а ожидался 400"

    with allure.step("Проверка структуры ошибки"):
        errors = response.json()

        # Проверка только первого поля, так как второе не валидируется
        assert "password1" in errors, "Нет сообщения об ошибке в поле password1"
        assert isinstance(errors["password1"], list), "Ошибка должна быть списком"
        assert len(errors["password1"]) >= 1, "Нет текста ошибки"
        
