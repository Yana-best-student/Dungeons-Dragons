import allure
import requests
import json
import os.path
import os
from dotenv import load_dotenv

load_dotenv()

# Базовый URL из переменных окружения
BASE_API_URL = os.getenv('API_URL')

# Полный URL регистрации
registration_url = BASE_API_URL + "/api/v1/auth/registration/"

# Заголовки запроса
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


@allure.epic("Dungeons-Dragons")
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Регистрация с недопустимым логином")
@allure.title("Регистрация с тире в поле логина")
@allure.description(
    "Тест проверяет реакцию системы на попытку регистрации с тире в поле логина. "
    "Ожидается отказ регистрации."
)
def test_invalid_login_dash():
    """
    Тест регистрирует нового пользователя с тире в поле логина.
    Ожидается отказ регистрации.
    """

    # Логин — пустая строка
    empty_username = "---"

    # Данные для регистрации
    payload = {
        'username': empty_username,  # Тире в поле логин
        'email': 'testuser123@gmail.com',
        'password1': 'Qaz159753@',
        'password2': 'Qaz159753@',
        'light_theme': False,
        'dark_theme': True
    }

    json_payload = json.dumps(payload)

    with allure.step("Отправить запрос на регистрацию с тире в поле  логин"):
        response = requests.post(registration_url, data=json_payload, headers=HEADERS)

        # Прикрепляем запрос и ответ к отчёту
        allure.attach(json_payload, name="Запрос", attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить статус ответа"):
        # Ожидаем ошибку (статус 400)
        assert response.status_code == 400, \
            f"Ожидался статус 400, но получен: {response.status_code}"

        # Прикрепляем статус-код к отчёту
        allure.attach(str(response.status_code), name="HTTP Status Code", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить сообщение об ошибке"):
        response_json = response.json()
    
    # Изменённая проверка
    assert "must contain only letters, numbers and underscores" in response_json["username"][0], \
           f"Ожидалось сообщение, содержащее фразу 'must contain only letters, numbers and underscores', но получено: {response_json['username'][0]}"