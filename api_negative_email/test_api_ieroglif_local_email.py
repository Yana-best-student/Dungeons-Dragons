import allure
import requests
import os
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv('API_URL')
if not BASE_API_URL:
    raise ValueError("Переменная окружения API_URL не установлена.")

REGISTRATION_URL = f"{BASE_API_URL}/api/v1/auth/registration/"
HEADERS = {'accept': 'application/json'}


@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с недопустимым email")
@allure.title("Регистрация email с иероглифом в локальной части")
@allure.description("""
Тест проверяет реакцию системы на попытку регистрации с email, содержащим иероглиф в локальной части.
Ожидается отказ регистрации с соответствующим сообщением об ошибке.
""")
@allure.tag("Negative", "EmailValidation", "Registration")
def test_invalid_local_email_with_chinese_character():
    """
    Негативный тест регистрации с email, содержащим иероглиф в локальной части.
    Ожидается отказ регистрации с сообщением об ошибке.
    """

    # Недопустимый email (иероглиф в локальной части)
    invalid_email = "sales丟support@megaplast.com"

    payload = {
        'username': "test_user",  # Можете сделать уникальное имя пользователя
        'email': invalid_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    with allure.step(f"Отправка запроса на регистрацию с email '{invalid_email}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)
        allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка отказа регистрации"):
        # Ожидаем ошибку валидации (статус 400)
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"

        # Распарсим JSON-ответ
        response_json = response.json()
        allure.attach(str(response_json), name="JSON Ответ", attachment_type=allure.attachment_type.JSON)

        # Проверяем, что в ответе есть поле email с ошибкой
        assert "email" in response_json, "В ответе нет поля 'email' с ошибкой"

        # Проверяем, что поле email содержит массив с ошибками
        assert isinstance(response_json["email"], list), "Поле 'email' должно быть списком"
        assert len(response_json["email"]) > 0, "Список ошибок для email пустой"

        # Проверяем текст ошибки
        possible_errors = [
            "Введите правильный адрес электронной почты.",
            "Enter a valid email address.",
            "Enter a valid email address"
        ]

        actual_error = response_json["email"][0]
        assert any(error in actual_error for error in possible_errors), \
            f"Ожидалось одно из сообщений: {possible_errors}, Получено: '{actual_error}'"