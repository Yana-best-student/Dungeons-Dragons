import allure
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем нужные переменные окружения
API_URL = os.getenv('API_URL')  # Базовый URL API
API_TOKEN = os.getenv('API_TOKEN')  # Токен авторизации (если используется)

# Проверяем наличие нужных переменных
if not API_URL or not API_TOKEN:
    raise ValueError("Отсутствуют обязательные переменные окружения.")

# Функция для получения CSRF и cookie


def get_csrf_and_cookie(API_URL):
    """
    Получает CSRF-токен и cookie с начальной страницы приложения.
    Возвращает кортеж (csrf_token, session_id).
    """
    # Адрес для получения CSRF и cookie (обычно главная страница или /login/)
    login_page_url = f"{API_URL}api/v1/auth/logout/"

    # Выполняем GET-запрос для получения cookie и CSRF
    response = requests.get(login_page_url)

    # Проверяем успешность запроса
    if response.status_code != 200:
        raise Exception(
            f"Ошибка получения CSRF и cookie: {response.status_code}")

    # Извлекаем CSRF-токен и session_id из cookies
    csrf_token = response.cookies.get("csrftoken")
    session_id = response.cookies.get("sessionid")

    return csrf_token, session_id


@allure.epic("Dungeons & Dragons")
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite("Авторизация пользователей")
@allure.story("Выход пользователя из системы")
@allure.title("Завершение сессии пользователя в игре Dungeons & Dragons")
@allure.description(
    "Тест проверяет возможность успешного завершения сессии авторизованного пользователя."
)
def test_logout():
    """Завершение сессии пользователя"""

    # Получаем CSRF и cookie динамически
    csrf_token, session_id = get_csrf_and_cookie(API_URL)

    # Формируем URL выхода
    logout_url = f"{API_URL}api/v1/auth/logout/"

    # Формируем правильные заголовки с динамическими значениями
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': csrf_token,
        'Cookie': f'sessionid={session_id}; csrftoken={csrf_token}'
    }

    # Готовим пустой payload (POST-данные)
    payload = {}  # Можно оставить пустым, если сервер ожидает пустой объект
    json_payload = json.dumps(payload)

    # Шаг тестирования: отправляем запрос на выход
    with allure.step("Отправка запроса на выход пользователя"):
        response = requests.post(
            logout_url, data=json_payload, headers=headers)

        # Прикрепляем запросы и ответы к отчету Allure
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.TEXT)

    # Шаг проверки результата
    with allure.step("Проверка успешности выхода"):
        assert response.status_code == 200, f"Ошибка выхода: {response.status_code}"
        allure.attach(str(response.status_code), name="HTTP Status Code",
                      attachment_type=allure.attachment_type.TEXT)