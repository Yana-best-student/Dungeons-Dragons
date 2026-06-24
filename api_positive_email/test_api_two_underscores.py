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

# === Основной тестовый метод ===
@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с валидным email")
@allure.title("Регистрация email c несколькими нижними подчёркиваниями в локальной части")
@allure.description("""
Тест проверяет успешную регистрацию пользователя с email, содержащим несколько нижних подчёркиваний в локальной части.
Ожидается успешная регистрация (статус 201).
""")
@allure.tag("Positive", "EmailValidation", "Registration")
def test_valid_local_email_with_multiple_underscores():
    """
    Позитивный тест успешной регистрации с email, содержащим несколько нижних подчёркиваний в локальной части.
    Ожидается успешная регистрация (статус 201).
    """

    # Валидный email с несколькими нижними подчёркиваниями в локальной части
    valid_email = "ivan__ivan@example.com"  # Три подчёркивания подряд

    payload = {
        'username': "valid_user",  # Можете сделать уникальное имя пользователя
        'email': valid_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    with allure.step(f"Отправка запроса на регистрацию с email '{valid_email}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)
        allure.attach(str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка успешного ответа сервера"):
        # Ожидаем успешную регистрацию (статус 201)
        assert response.status_code == 201, f"Ожидался статус 201, получен: {response.status_code}"

        # Парсим JSON-ответ
        response_json = response.json()

        # === Исправленная проверка ===
        # Убираем проверку поля pk, так как его нет в ответе
        # assert "pk" in response_json, "В ответе нет поля 'pk'"  # <-- Эту строчку удаляем

        # Проверяем, что в ответе есть поле user
        assert "user" in response_json, "В ответе нет поля 'user'"

        # Проверяем, что в объекте user есть email
        assert "email" in response_json["user"], "В ответе нет email пользователя"

        # Опционально: можно проверить, что пароль не возвращается в открытом виде
        assert "password" not in response_json, "Пароль не должен возвращаться в ответе"