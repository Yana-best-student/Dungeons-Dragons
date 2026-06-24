import datetime as dt
import os
import pytest
import requests
import allure
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получаем базовый URL из переменной окружения. Если она не задана, оставляем пустую строку.
# Это предотвратит ошибку при конкатенации, но сам запрос, скорее всего, упадет.
BASE_API_URL = os.getenv('API_URL') or ''
REGISTRATION_URL = f'{BASE_API_URL}/api/v1/auth/registration/'
HEADERS = {'accept': 'application/json'}


@pytest.mark.xfail(reason='Сервер допускает некорректный email, ожидается отказ.')
@allure.epic('Dungeons & Dragons')
@allure.feature('Авторизация и регистрация')
@allure.story('Регистрация с недопустимым email')
@allure.tag('Negative', 'EmailValidation', 'Registration')

# Используем параметризацию для запуска одного теста с разными данными
@pytest.mark.parametrize(
    'email',
    ['_ivan@example.com', 'ivan_@example.com'],
    ids=['Подчёркивание в начале локальной части', 'Подчёркивание в конце локальной части']
)
def test_invalid_email_with_underscore(email):
    """
    Негативный тест: проверка, что сервер отклоняет регистрацию с email,
    где '_' находится в начале или конце локальной части.
    """

    # Генерируем уникальное имя пользователя на основе текущего времени
    now = int(dt.datetime.now().timestamp())
    username = f'test_user_{now}'

    payload = {
        'username': username,
        'email': email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    with allure.step(f'Отправка запроса на регистрацию с email "{email}"'):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)
        
        # Прикрепляем к отчету Allure тело запроса и ответа для анализа
        allure.attach(str(payload), name='Запрос', attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name='Ответ', attachment_type=allure.attachment_type.TEXT)

    with allure.step('Проверка ответа сервера на ошибку валидации'):
        # 1. Проверяем, что сервер вернул статус-код ошибки клиента (400)
        assert response.status_code == 400, f'Ожидался статус 400 (Bad Request), получен: {response.status_code}'

        # Парсим JSON-ответ. Используем try-except на случай, если ответ не в формате JSON.
        try:
            response_json = response.json()
        except ValueError:
            assert False, "Ответ от сервера не является валидным JSON"

        # 2. Безопасно получаем список ошибок для поля 'email'
        errors = response_json.get('email')
        
        # Проверяем, что поле 'email' есть в ответе и оно содержит список ошибок
        assert errors is not None, "В ответе отсутствует поле 'email' с описанием ошибок"
        assert isinstance(errors, list), "Поле 'email' должно содержать список ошибок"
        assert len(errors) > 0, "Список ошибок поля 'email' пуст"

        # 3. Проверяем текст первой ошибки в списке
        actual_error = errors[0].lower()
        assert 'valid email' in actual_error, f"Ожидалась ошибка валидации email. Получено: '{actual_error}'"