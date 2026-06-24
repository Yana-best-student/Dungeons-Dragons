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
@allure.story("Регистрация с несовпадающим паролем")
@allure.title("Ошибка при регистрации пользователя с паролем из 7 символов")
@allure.description(
    "Минимальная длина пароля — 8 символов. Этот тест проверяет, что регистрация с меньшим количеством символов невозможна."
)
@allure.title("Несовпадающие пароли")
@allure.description(
    "Тест проверяет, что API возвращает ошибку 400, если введено два разных пароля."
)
@pytest.mark.xfail(
    reason="Bug #1234: API некорректно обрабатывает разные пароли. Ждем фикса.",
    run=True,
    strict=False
)
def test_mismatch_passwords():
    """Тест проверяет, что система отклоняет разные пароли.
    !!! БАГ !!!
    Сейчас тест проходит (201), хотя должен выдавать ошибку 400.
    Причина: в эндпоинте auth/registration/ нет встроенного валидатора.
    """

    unique_part = os.urandom(4).hex()
    username = f"test_user_{unique_part}"
    email = f"test_email_{unique_part}@example.com"

    payload = {
        "username": username,
        "email": email,
        "password1": "ValidPassword1!",
        "password2": "AnotherValidPassword!",  # Другой пароль
        "light_theme": False,
        "dark_theme": True
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

        # Ошибка должна прийти именно по полю non_field_errors
        assert "non_field_errors" in errors, "Нет сообщения об ошибке"
        assert isinstance(errors["non_field_errors"], list), "Ошибка должна быть списком"
        assert len(errors["non_field_errors"]) >= 1, "Нет текста ошибки"