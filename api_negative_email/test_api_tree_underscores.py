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

@pytest.mark.xfail(reason="Баг на бэкенде: API принимает email с тремя подчеркиваниями. Ожидаемый статус 400.")
@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с невалидным email")
@allure.title(
    "Негативная проверка: Регистрация c тремя нижними подчёркиваниями подряд в локальной части email"
)
@allure.description("""
Тест проверяет, что система корректно отклоняет регистрацию пользователя,
если в локальной части email-адреса содержатся три или более нижних подчёркивания подряд.
Ожидается ошибка валидации (статус 400) и отсутствие поля 'user' в теле ответа.
""")
@allure.tag("Negative", "EmailValidation", "Registration")


def test_invalid_local_email_with_multiple_underscores():
    """
    Негативный тест для проверки валидации email.
    Ожидается, что регистрация будет отклонена из-за некорректного формата email.
    """
    
    invalid_email = "invalid___user@example.com"
    
    payload = {
        'username': "test_user",
        'email': invalid_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    with allure.step(f"Отправка запроса на регистрацию с некорректным email '{invalid_email}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)
        allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка ответа сервера на ошибку валидации"):
        # Ожидаем ошибку клиента из-за неверных данных (400 Bad Request)
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"