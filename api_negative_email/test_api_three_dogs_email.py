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
@allure.title("Регистрация email c недопустимыми символами @@@")
@allure.description("""
Тест проверяет реакцию системы на попытку регистрации email c недопустимыми символами@@@.
Ожидается отказ регистрации с соответствующим сообщением об ошибке.
""")
@allure.tag("Negative", "EmailValidation", "Registration")
def test_invalid_local_email():
    # Используйте заведомо недопустимый email (три @ подряд)
    invalid_email = "ivanov@@@gmail.com"

    payload = {
        'username': "scorpio",
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

    with allure.step("Проверка ответа сервера"):
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"

        try:
            response_json = response.json()
            allure.attach(str(response_json), name="JSON Ответ", attachment_type=allure.attachment_type.JSON)
        except ValueError:
            pytest.fail("Ответ сервера не является валидным JSON")

        # Проверяем наличие поля email с ошибкой
        assert "email" in response_json, "В ответе нет поля 'email' с ошибкой"

        # Проверяем, что поле email содержит массив с ошибками
        assert isinstance(response_json["email"], list), "Поле 'email' должно быть списком"
        assert len(response_json["email"]) > 0, "Список ошибок для email пустой"

        # Список возможных ошибок валидации email
        possible_errors = [
            "Введите правильный адрес электронной почты.",
            "Enter a valid email address.",
            "Enter a valid email address"
        ]

        # Проверяем, что хотя бы одна из возможных ошибок присутствует
        actual_error = response_json["email"][0]
        assert any(error in actual_error for error in possible_errors), \
            f"Ожидалось одно из сообщений: {possible_errors}, Получено: '{actual_error}'"