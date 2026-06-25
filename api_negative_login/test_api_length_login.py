import datetime as dt
import os
import pytest
import requests
import allure
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv('API_URL') or ''
REGISTRATION_URL = f'{BASE_API_URL}/api/v1/auth/registration/'
HEADERS = {'accept': 'application/json'}

@allure.epic("Dungeons & Dragons")
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Регистрация с недопустимым логином")
@allure.title("Регистрация с логином, разной длины")
@allure.description(
    "Тест проверяет реакцию системы на попытку регистрации с логином разной длины."
     "Ожидается отказ регистрации."
)

# Добавляем новый набор проверок для длины логина
@pytest.mark.parametrize(
    "username",
    [
        "", # Пустой логин
        "a", # Слишком короткий (если есть ограничение)
        "a" * 31, # Слишком длинный (превышение лимита в 30 символов)
        "a" * 1000 # Очень длинная строка (проверка на DoS)
    ],
    ids=[
        "Пустой логин",
        "Логин из 1 символа",
        "Логин из 31 символа",
        "Логин из 1000 символов"
    ]
)
def test_username_length_validation(username):
    """
    Негативный тест: проверка реакции API на некорректную длину логина.
    """
    # Генерируем уникальный email для каждого прогона
    now = int(dt.datetime.now().timestamp())
    email = f'test_email_{now}@example.com'

    payload = {
        'username': username,
        'email': email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
    }

    with allure.step(f"Отправка запроса с логином '{username}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)
        allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка ответа сервера"):
        # Ожидаем ошибку валидации для всех этих случаев
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"