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
@allure.severity(allure.severity_level.MINOR)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Регистрация с длинными паролями")
@allure.title("Ошибка при создании пользователя с паролем из 42 символов (слэши)")
@allure.description(
    "Максимально допустимая длина пароля — 40 символов. Тест проверяет, что слэш (/) не ломает валидацию."
)
def test_long_password_with_slashes():
    """Тест проверяет, что система отклоняет длинный пароль с символами //"""

    unique_part = os.urandom(4).hex()
    username = f"test_user_{unique_part}"
    email = f"test_email_{unique_part}@example.com"

    long_password = (
        "//Long2023passwor//dWithSlashesAndSpecialChars//"
    )  # 42 символа

    payload = {
        "username": username,
        "email": email,
        "password1": long_password,
        "password2": long_password,
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