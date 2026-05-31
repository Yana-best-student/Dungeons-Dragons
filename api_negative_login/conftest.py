# conftest.py

import pytest
import requests
import os

# Базовый URL проекта (можно загрузить из .env)
BASE_API_URL = os.getenv('API_URL')

# Endpoint для удаления пользователя (укажите реальный путь)
USER_DELETE_ENDPOINT = '/api/v1/users/delete/'

# Заголовки запроса (можно загрузить из .env)
HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-CSRFToken': os.getenv('CSRF_TOKEN')
}

# Фикстура для автоматической очистки пользователя после теста
@pytest.fixture(scope='function', autouse=True)
def cleanup_user(request):
    """
    Фикстура для автоматической очистки пользователя после каждого теста
    Работает на уровне функции (после каждого теста)
    """
    
    # Переменная для хранения ID пользователя
    request.node.user_id = None
    
    yield  # Эта точка отмечает завершение фазы setup (до теста)
    
    # Фаза teardown (после теста)
    if request.node.user_id:
        # Удаляем пользователя через API
        delete_response = requests.delete(
            f"{BASE_API_URL}{USER_DELETE_ENDPOINT}{request.node.user_id}/",
            headers=HEADERS
        )
        
        # Контролируем успешность удаления
        assert delete_response.status_code == 204, \
            f"Не удалось удалить пользователя ({delete_response.status_code}). " \
            f"Ответ: {delete_response.text}"
        
        print(f"Пользователь с ID={request.node.user_id} успешно удалён")