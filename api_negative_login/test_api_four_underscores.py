# test_api_four_underscores.py

import allure
import requests
import pytest
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv('API_URL')
REGISTRATION_ENDPOINT = '/api/v1/auth/registration/'
REGISTRATION_URL = BASE_API_URL + REGISTRATION_ENDPOINT

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': os.getenv('CSRF_TOKEN')
}


@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Недопустимый логин")
@allure.title("Отказ регистрации с логином '____'")
def test_login_with_4_underscores_is_invalid():
    """Проверка блокировки логина '____'."""

    payload = {
        "username": "____",
        "email": f"test-{uuid.uuid4()}@example.com",
        "password1": "StrongP@ssw0rd!",
        "password2": "StrongP@ssw0rd!"
    }

    response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)

    with allure.step("Анализ ответа сервера"):
        # 📊 Сохраняем ответ в отчёт
        allure.attach(
            str(response.json()),
            name="Полный ответ сервера",
            attachment_type=allure.attachment_type.JSON
        )

        assert response.status_code == 400, (
            f"Сценарий: логин '____' должен быть заблокирован.\n"
            f"Получено: статус {response.status_code}, "
            f"сообщение: {response.text[:100]}"
        )
