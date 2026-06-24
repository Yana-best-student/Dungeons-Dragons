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
@allure.story("Регистрация с длинным паролем")
@allure.title("Ошибка при создании пользователя с паролем из 75 символов")
@allure.description(
    "Тест проверяет отказ системы при попытке зарегистрировать пользователя "
    "с паролем максимальной длины (75 символов)"
)
@pytest.mark.xfail(
    reason="Сервер ошибочно создает аккаунт с паролем из 75 символов.",
    raises=AssertionError,
    run=True,
    strict=False
)
def test_long_password_error():
    """Тест проверяет, что система отклоняет пароль из 75 символов."""

    # ✅ Генерация данных
    unique_part = os.urandom(4).hex()
    username = f'test_user_{unique_part}'
    email = f'test_email_{unique_part}@example.com'

    long_password = (
        'Lorem2023ipsumdolorsitametconsecteturadipiscingelitAenean'
        'commodoLigulaegetdolorAliquam'
    )

    payload = {
        'username': username,
        'email': email,
        'password1': long_password,
        'password2': long_password,
        'light_theme': False,
        'dark_theme': True
    }

    with allure.step("Отправка запроса на регистрацию"):
        response = requests.post(
            registration_url, data=json.dumps(payload), headers=HEADERS)
        allure.attach(json.dumps(payload, indent=2), name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 400, \
            f'Статус должен быть 400, а пришел {response.status_code}'

    with allure.step("Проверка структуры ошибки"):
        errors = response.json()
        assert 'password1' in errors, 'Не найдено сообщение об ошибке в поле password1'
        assert 'password2' in errors, 'Не найдено сообщение об ошибке в поле password2'
