import allure
import requests
import json
import os.path
import os
from dotenv import load_dotenv, set_key

load_dotenv()

# Получаем базовый URL из переменных окружения
# Должен быть установлен как https://api.test.dnd.ktsf.ru/
BASE_API_URL = os.getenv('API_URL')

# Формируем полный URL регистрации
registration_url = BASE_API_URL + "/api/v1/auth/registration/"

# Заголовки запроса
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    # Остальные заголовки (CSRF и Cookie) добавлять не нужно, если не требуются
}


@allure.epic("Dungeons-Dragons")
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite("Тесты на регистрацию пользователей")
@allure.story("Создание нового пользователя")
@allure.title("Регистрация нового пользователя в игре")
@allure.description(
    "Тест проверяет успешную регистрацию нового пользователя в игре."
)
def test_registration():
    """
    Тест регистрирует нового пользователя с конкретными данными.
    """

    # Жёстко заданные данные для регистрации
    payload = {
        'username': 'scorpio666',
        'email': 'yascorpio777@gmail.com',
        'password1': 'Qaz159753@',
        'password2': 'Qaz159753@',
        'light_theme': False,
        'dark_theme': True
    }

    json_payload = json.dumps(payload)

    with allure.step("Отправить запрос на регистрацию пользователя"):
        response = requests.post(
            registration_url, data=json_payload, headers=HEADERS)
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить статус ответа"):
        assert response.status_code == 201, f"Некорректный статус: {response.status_code}"
        allure.attach(str(response.status_code), name="HTTP Status Code",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Сохранить токены в переменные окружения"):
        response_json = response.json()

        project_root = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(project_root, '..', '.env')

        # Обновляем или добавляем токены в .env
        with open(env_path, 'r') as f:
            lines = f.readlines()

        updated_lines = []
        access_token_found = False
        refresh_token_found = False

        for line in lines:
            if line.startswith('ACCESS_TOKEN='):
                updated_lines.append(
                    f"ACCESS_TOKEN={response_json['access']}\n")
                access_token_found = True
            elif line.startswith('REFRESH_TOKEN='):
                updated_lines.append(
                    f"REFRESH_TOKEN={response_json['refresh']}\n")
                refresh_token_found = True
            else:
                updated_lines.append(line)

        if not access_token_found:
            updated_lines.append(f"ACCESS_TOKEN={response_json['access']}\n")
        if not refresh_token_found:
            updated_lines.append(f"REFRESH_TOKEN={response_json['refresh']}\n")

        with open(env_path, 'w') as f:
            f.writelines(updated_lines)

        allure.attach(response_json['access'], name="Access Token",
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(response_json['refresh'], name="Refresh Token",
                      attachment_type=allure.attachment_type.TEXT)
