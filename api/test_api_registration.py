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
def test_successful_registration():
    """
    Тест регистрирует нового пользователя с уникальными данными.
    """

    # Генерируем уникальные данные для регистрации
    unique_part = os.urandom(4).hex()
    username = f"test_user_{unique_part}"
    email = f"test_email_{unique_part}@example.com"

    # Данные для регистрации
    payload = {
        'username': username,
        'email': email,
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
        'light_theme': False,
        'dark_theme': True
    }

    # Преобразуем payload в JSON
    json_payload = json.dumps(payload)

    with allure.step("Отправить запрос на регистрацию пользователя"):
        # Отправляем POST-запрос с JSON-телом
        response = requests.post(
            registration_url, data=json_payload, headers=HEADERS)

        # Прикрепляем запрос и ответ к отчёту Allure
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.text), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить статус ответа"):
        # Проверяем статус-код
        assert response.status_code == 201, f"Некорректный статус: {response.status_code}"
        allure.attach(str(response.status_code), name="HTTP Status Code",
                      attachment_type=allure.attachment_type.TEXT)

    with allure.step("Сохранить токены в переменные окружения"):
        response_json = response.json()
    
    # 🟢 КОМБИНИРОВАННЫЙ ПОДХОД: ЧТЕНИЕ + ОБНОВЛЕНИЕ + ЗАПИСЬ
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(project_root, '..', '.env')
    
    # Читаем текущий файл .env
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Обновляем токены в списке строк
    updated_lines = []
    for line in lines:
        if line.startswith('ACCESS_TOKEN='):
            updated_lines.append(f"ACCESS_TOKEN={response_json['access']}\n")
        elif line.startswith('REFRESH_TOKEN='):
            updated_lines.append(f"REFRESH_TOKEN={response_json['refresh']}\n")
        else:
            updated_lines.append(line)
    
    # Добавляем токены, если их ещё нет в файле
    if not any(line.startswith('ACCESS_TOKEN=') for line in lines):
        updated_lines.append(f"ACCESS_TOKEN={response_json['access']}\n")
    if not any(line.startswith('REFRESH_TOKEN=') for line in lines):
        updated_lines.append(f"REFRESH_TOKEN={response_json['refresh']}\n")
    
    # Перезаписываем файл .env
    with open(env_path, 'w') as f:
        f.writelines(updated_lines)
    
    # Прикрепляем новые токены к отчету
    allure.attach(response_json['access'], name="Access Token",
                  attachment_type=allure.attachment_type.TEXT)
    allure.attach(response_json['refresh'], name="Refresh Token",
                  attachment_type=allure.attachment_type.TEXT)
