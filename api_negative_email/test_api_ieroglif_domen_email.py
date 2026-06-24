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


# @pytest.mark.xfail(reason='Backend не проверяет доменную часть email.')
@allure.epic("Dungeons & Dragons")
@allure.feature("Авторизация и регистрация")
@allure.story("Регистрация с недопустимым email")
@allure.title("Регистрация email с иероглифом в домене")
@allure.description("""
Тест проверяет реакцию системы на email с иероглифом в доменном имени.
Сервер должен вернуть ошибку 400.
""")
@allure.tag("Negative", "EmailValidation", "Registration")
def test_invalid_domain_email_with_chinese_character():
    """Негативный тест регистрации с email, содержащим иероглиф в домене."""

    # Подготовка данных
    invalid_email = "staff@travel丟users.com"

    payload = {
        'username': "test_user",
        'email': invalid_email,
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'light_theme': False,
        'dark_theme': True
    }

    # Отправка запроса
    with allure.step(f"Отправка запроса с email '{invalid_email}'"):
        response = requests.post(REGISTRATION_URL, json=payload, headers=HEADERS)

        # 🎯 Прикрепляем запросы и ответы
        allure.attach(
            str(payload), name="Запрос", attachment_type=allure.attachment_type.JSON
        )

        try:
            # Пробуем разобрать ответ как JSON
            resp_body = response.json()
            allure.attach(
                str(resp_body), name=f"Ответ ({response.status_code})", attachment_type=allure.attachment_type.JSON
            )
        except Exception:
            # Если пришел обычный текст (HTML, XML)
            allure.attach(
                str(response.text), name=f"Ответ ({response.status_code})", attachment_type=allure.attachment_type.TEXT
            )

    # Проверка результата
    with allure.step("Проверка отказа регистрации"):
        # Проверка статуса
        assert response.status_code == 400, (
            f"\n⛔ Тест упал! Сервер принял недопустимый email!\n"
            f"Получен статус: {response.status_code}.\n"
            f"Ожидался статус: 400."
        )

        # Проверка содержания ошибки
        errors = resp_body.get('email') or []
        assert isinstance(errors, list), "✖ Поле 'email' должно быть списком!"
        assert errors != [], "✖ Список ошибок для email пустой."

        # Проверка текста ошибки
        actual_text = errors[0].strip().lower()
        expected_words = ['валидный', 'valid', 'correct']
        assert any(word in actual_text for word in expected_words), (
            f"\n✖ Ошибка не совпадает с ожиданием!\n"
            f"Получено: '{actual_text}'.\n"
            f"Должно быть слово из списка: {expected_words}"
        )