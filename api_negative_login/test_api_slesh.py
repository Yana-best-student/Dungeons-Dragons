import allure
import requests
import json
import os.path
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем базовый URL из переменных окружения
BASE_API_URL = os.getenv('API_URL')

# Формируем полный URL регистрации
registration_url = BASE_API_URL + "/api/v1/auth/registration/"

# Заголовки запроса
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}


@allure.epic("Dungeons-Dragons")
@allure.severity(allure.severity_level.NORMAL)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Регистрация с недопустимым логином")
@allure.title("Регистрация с логином, содержащим символы ///")
@allure.description(
    "Тест проверяет реакцию системы на попытку регистрации с логином, "
    "содержащим символы ///."
)
def test_invalid_login_with_slashes():
    """
    Тест регистрирует нового пользователя с логином, содержащим символы ///.
    Ожидается отказ регистрации.
    """

    # Логин с недопустимыми символами
    invalid_username = "///"

    # Данные для регистрации
    payload = {
        'username': invalid_username,  # Недопустимый логин
        'email': 'testuser123@gmail.com',
        'password1': 'Qaz159753@',
        'password2': 'Qaz159753@',
        'light_theme': False,
        'dark_theme': True
    }

    json_payload = json.dumps(payload)

    with allure.step("Отправить запрос на регистрацию с недопустимым логином"):
        response = requests.post(
            registration_url, data=json_payload, headers=HEADERS)

        # Прикрепляем запрос и ответ к отчёту
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить статус ответа"):
        # Ожидаем ошибку (например, статус 400)
        assert response.status_code == 400, \
            f"Ожидалась ошибка (400), но получен статус: {response.status_code}"

        # Прикрепляем статус-код к отчёту
        allure.attach(str(response.status_code), name="HTTP Status Code",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверить сообщение об ошибке"):
        response_json = response.json()
        
        # Проверяем, что в ответе есть поле "username" с сообщением об ошибке
        assert isinstance(response_json["username"], list), "Поле 'username' не является массивом"
        assert len(response_json["username"]) > 0, "Массив 'username' пустой"
        
        # Проверяем текст сообщения об ошибке
        expected_error_message = "Username must contain only letters, numbers and underscores."
        assert response_json["username"][0] == expected_error_message, \
            f"Ожидалось сообщение '{expected_error_message}', но получено: {response_json['username'][0]}"
        
        # Прикрепляем сообщение об ошибке к отчёту
        allure.attach(response_json["username"][0], name="Сообщение об ошибке",
                      attachment_type=allure.attachment_type.TEXT)