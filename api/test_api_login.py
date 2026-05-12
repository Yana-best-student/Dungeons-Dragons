import allure
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Получаем URL и токен из переменных окружения
API_URL = os.getenv('API_URL')
# Предполагается, что этот токен будет использоваться позже
API_TOKEN = os.getenv('API_TOKEN')

if API_URL is None:
    raise ValueError("Переменная окружения 'API_URL' не найдена")

login_url = f"{API_URL}api/v1/auth/login/"

# Заголовки запроса
HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',  # Тип передаваемых данных
    'X-CSRFToken': '4nm5Mlhs720LVH3buJ1ImNdQ4uTOMNfpS5goUTONMpBaSIgmPMItwcpenRoiZnKlgE',  # Токен CSRF
    'Cookie': (
        '_yhtoken=yh-wz7TEGY7JG7B-AhSSPNumEWYPODTJaQs;'  # Значение cookie
        'messages=eixVFFEKCAoGAQRi-yIRallnsSZayI4ykufJH_YyzZ'
        '4xZOogSw2XZHMeeIsFyWynsvKdvcVCVOOYimkg_whIz4z'
        'HIElJeibXTvyIMhc20THuWH20Egct6IExtBVelyMR'
        's:i1Khkf:EmgstMeST57yo_qVtefcBg8t800oyglIAN-gqV'
        'RaUHhs; sessionid=elvvubuyffyy'
        'x73dblf3nvfct0ngsv'
    ),
    # Используем API_TOKEN, если он нужен
    'Authorization': f'Token {API_TOKEN}'
}


@allure.epic("Dungeons-Dragons")
@allure.severity(allure.severity_level.CRITICAL)
@allure.suite("Тесты на авторизацию в игре")
@allure.story("Авторизация в игре с паролем и почтой")
@allure.title("Авторизация в игре Dungeons-Dragons")
@allure.description(
    "Тест проверяет возможность авторизации пользователя в игре."
)
def test_authorization():
    """
    Авторизация пользователя в игре.
    :param: Передаем тело запроса в формате JSON.
    """
    # Данные для аутентификации
    payload = {
        'username': 'scorpio666',
        'email': 'yascorpio777@gmail.com',
        'password': 'Qaz159753@'
    }

    # Преобразуем payload в JSON
    json_payload = json.dumps(payload)

    with allure.step("Отправить запрос на авторизацию пользователя"):
        # Отправляем POST-запрос с JSON-телом
        response = requests.post(login_url, data=json_payload, headers=HEADERS)

        # Прикрепляем запрос и ответ к отчёту Allure
        allure.attach(json_payload, name="Запрос",
                      attachment_type=allure.attachment_type.JSON)
        allure.attach(str(response.content.decode()), name="Ответ",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить статус ответа"):
        # Проверяем статус-код
        assert response.status_code == 200, f"Некорректный статус: {response.status_code}"
        allure.attach(str(response.status_code), name="HTTP Status Code",
                      attachment_type=allure.attachment_type.TEXT)
