import allure
import requests
import os
import pytest
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Базовый URL проекта
BASE_API_URL = os.getenv('API_URL')
if not BASE_API_URL:
    raise ValueError("Переменная окружения API_URL не установлена.")

# Эндпоинт регистрации
REGISTRATION_URL = f"{BASE_API_URL}/api/v1/auth/registration/"
HEADERS = {'accept': 'application/json'}

# Основной тестовый метод


@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с недопустимым email")
@allure.title("Регистрация с email c пустой строкой")
@allure.description("""
Тест проверяет реакцию системы на попытку регистрации с email c пустой строкой.
Ожидается отказ регистрации с соответствующим сообщением об ошибке.
""")
@allure.tag("Negative", "EmailValidation", "Registration")
def test_invalid_local_email():
    """
    Негативный тест регистрации с недопустимым email (c пустой строкой).
    Ожидается отказ регистрации с сообщением об ошибке.
    """

    # Недопустимый email (пустая строка)
    invalid_email = " "

    # Формирование тела запроса
    payload = {
        'username': "scorpio",
        'email': invalid_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    # Отправка POST-запроса на регистрацию
    with allure.step(f"Отправка запроса на регистрацию с email '{invalid_email}'"):
        response = requests.post(
            REGISTRATION_URL, json=payload, headers=HEADERS)

        # Прикрепление запроса и ответа к отчёту
        allure.attach(str(payload), name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.TEXT)

    # Проверка статуса и тела ответа
    with allure.step("Проверка ответа сервера"):
        # Ожидаем ошибку валидации (обычно 400)
        assert response.status_code == 400, f"Ожидался статус 400, получен: {response.status_code}"

        # Попытка распарсить JSON. Обернём в try-except на случай некорректного ответа.
        try:
            response_json = response.json()
            allure.attach(str(response_json), name="JSON Ответ",
                          attachment_type=allure.attachment_type.JSON)
        except ValueError:
            pytest.fail("Ответ сервера не является валидным JSON")

        # --- ОПТИМИЗИРОВАННЫЕ ПРОВЕРКИ ---
        # Проверяем наличие ошибки именно в поле email
        assert "email" in response_json, "В ответе нет поля 'email' с ошибкой"

        # Ожидаем массив с описанием ошибки
        assert isinstance(response_json["email"],
                          list), "Поле 'email' должно быть списком"
        assert len(response_json["email"]
                   ) > 0, "Список ошибок для email пустой"

        # Тексты ошибок могут отличаться в зависимости от локализации
        # Мы ожидаем, что сообщение об ошибке говорит что email пустой/некорректный.
        possible_errors = [
            "Email cannot be blank.",  # с точкой
            "Email cannot be blank"    # без точки
        ]

        # Нормализуем фактическое сообщение: удаляем ведущие/ trailing пробелы и конечную точку
        actual_error_raw = response_json["email"][0]
        actual_error_norm = actual_error_raw.strip().rstrip(".")

        # Сравниваем нормализованное сообщение с ожидаемыми формулировками
        assert any(actual_error_norm == err.rstrip(".") for err in possible_errors), \
            f"Ожидалось одно из сообщений: {possible_errors}, Получено: '{actual_error_raw}'"
