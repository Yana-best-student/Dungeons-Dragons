import allure
import requests
import json
import os
from dotenv import load_dotenv


# Загружаем переменные окружения
load_dotenv()

# Базовый URL
BASE_API_URL = os.getenv('API_URL')
CHANGE_PASSWORD_URL = BASE_API_URL + '/api/v1/auth/password/change/'

# Заголовки запроса
HEADERS = {
    'accept': 'application/json',
    'Authorization': f"Bearer {os.getenv('ACCESS_TOKEN')}",
    'Content-Type': 'application/json',
    'X-CSRFToken': os.getenv('CSRF_TOKEN'),
    'Cookie': os.getenv('COOKIE')
}

# Payload для смены пароля
PAYLOAD = {
    'new_password1': 'Wsx753159@',
    'new_password2': 'Wsx753159@'
}

# Преобразуем payload в JSON
json_payload = json.dumps(PAYLOAD)


@allure.epic("Dungeons & Dragons")
@allure.feature("Управление аккаунтом")
@allure.story("Смена пароля пользователя")
@allure.title("Автоматический тест: смена пароля пользователя")
@allure.description(
    "Тест проверяет успешную смену пароля пользователя через API."
)
def test_change_password():
    """Тест проверяет успешную смену пароля пользователя."""

    with allure.step("Подготовка данных для запроса"):
        # Привяжем payload и заголовки к отчёту
        allure.attach(json_payload, name="Payload", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(HEADERS), name="Headers", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Отправка POST-запроса на смену пароля"):
        # Отправляем POST-запрос
        response = requests.post(CHANGE_PASSWORD_URL, headers=HEADERS, data=json_payload)

        # Прикрепляем ответ к отчёту
        allure.attach(str(response.text), name="Response Body", attachment_type=allure.attachment_type.TEXT)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка статуса ответа"):
        # Проверяем, что пароль сменился успешно (статус 200 OK)
        assert response.status_code == 200, f"Ошибка: ожидался статус 200, получен {response.status_code}"

    with allure.step("Логирование успешного завершения теста"):
        allure.attach("Пароль успешно изменён.", name="Результат", attachment_type=allure.attachment_type.TEXT)