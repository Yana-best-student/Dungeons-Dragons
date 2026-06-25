"""
Тест проверяет, что сервер не позволяет зарегистрировать пользователя с логином, который уже есть в базе.
"""

import datetime as dt
import os
import pytest
import requests
import allure
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Базовый URL берем из переменной окружения
BASE_API_URL = os.getenv('API_URL')
if not BASE_API_URL:
    raise ValueError("Переменная окружения API_URL не установлена.")

# Составляем конечную точку для регистрации
REGISTRATION_URL = f"{BASE_API_URL}/api/v1/auth/registration/"
HEADERS = {'accept': 'application/json'}


# === ФИКСТУРА: Создаем реального пользователя ===
# Эта функция будет выполнена ДО запуска теста
@pytest.fixture(scope="function")
def existing_user():
    """
    Цель: создать пользователя с уникальным логином, чтобы им воспользоваться в основном тесте.
    """

    # Генерируем уникальное имя пользователя на основе текущего времени
    timestamp = str(int(dt.datetime.now().timestamp()))
    username = f"existing_user_{timestamp}"

    # Готовим данные для отправки
    payload = {
        "username": username,
        "email": f"{username}@example.com",
        "password1": "SuperSecurePassword123!",
        "password2": "SuperSecurePassword123!"  # Обязательное поле для подтверждения
    }

    # Отправляем POST-запрос на регистрацию
    response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)

    # Проверяем, что фикстура выполнилась успешно
    assert response.status_code == 201, f"Не удалось создать пользователя. Статус: {response.status_code}"

    # Возвращаем созданный логин, чтобы передать его в тест
    return {"username": username}


# === ОСНОВНОЙ ТЕСТ: Регистрация с занятым логином ===
@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с существующим логином")
@allure.title("Повторная регистрация с логином, который уже есть в БД")
@allure.tag("Negative", "LoginValidation", "Registration")
def test_registration_with_existing_login(existing_user):
    """
    Цель: доказать, что сервер не создает учетную запись, если логин уже занят.
    """

    # Берем логин из фикстуры (этот пользователь уже есть в базе)
    duplicate_username = existing_user["username"]

    # Готовим новый почтовый ящик, чтобы данные были валидными
    new_email = f"new_email_{dt.datetime.now().timestamp()}@example.com"

    # Формируем тело запроса (логин занят, email новый)
    payload = {
        "username": duplicate_username,
        "email": new_email,
        "password1": "AnotherStrongPassword123!",
        "password2": "AnotherStrongPassword123!"
    }

    # ШАГ 1: Отправка запроса
    with allure.step(f"Отправка запроса с логином '{duplicate_username}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)

        # Прикрепляем данные к отчету Allure
        allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.TEXT)

    # ШАГ 2: Проверка HTTP-статуса
    with allure.step("Проверка статуса ответа"):
        # Ожидаем ошибку клиента (400 Bad Request)
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"

    # ШАГ 3: Проверка структуры JSON-ответа
    with allure.step("Анализ тела ответа"):
        # Пробуем распарсить ответ как JSON
        response_json = {}
        try:
            response_json = response.json()
        except Exception as e:
            # Если пришел не JSON, тест падает
            assert False, f"Ответ от сервера не является JSON: {str(e)}. Текст: {response.text}"

        # Проверяем, что в ответе есть поле с ошибкой по логину
        assert "username" in response_json, "В ответе нет поля 'username'"
        errors = response_json["username"]

        # Проверяем, что это список и он не пустой
        assert isinstance(errors, list), "Поле 'username' должно быть списком"
        assert len(errors) > 0, "Список ошибок для 'username' пуст"

        # ШАГ 4: Проверка текста ошибки
        first_error = errors[0].strip().lower()
        # Варианты сообщений, которые может вернуть сервер
        acceptable_messages = ["already exists", "already taken", "занято"]
        assert any(msg in first_error for msg in acceptable_messages), \
            f"Текст ошибки отличается от ожидаемого. Получено: '{first_error}'"