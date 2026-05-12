# Dungeons-Dragons

## Шаблон для автоматизации тестирования на python

### Шаги

1. Склонировать проект `git clone [репозиторий](https://github.com/Yana-best-student/Dungeons-Dragons)`
2. Установить все зависимости pip3 install > -r requirements.txt
3. Запустить тесты 'pytest'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report'
5. Открыть отчет 'allure open allure-report'
6. Выполнить команду pip install -r requirements.txt в терминале.
7. Создать файл .env в корне проекта и добавить в него переменные:

- [API_URL](https://api.test.dnd.ktsf.ru/api/v1/auth/)
- API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTA1OTY5LCJpYXQiOjE3NzgwOTUxNjksImp0aSI6ImY3OWZmOTI5ZjhmYTQ5YzY5ZjJkNzc1MmUwYzNmNDU5IiwidXNlcl9pZCI6OH0.g1o-y8kdcOcSSdZsUSVxVRVC6ijglDDDMkTwlWyvv5c

### Стек

- pytest
- selenium
- requests
- sqlalchemy
- allure
- configparser
- json

### Структура

- ./test - тесты
- ./pages - описание страниц
- ./api - хелперы для работы с API
- ./db - хелперы для работы с БД
- ./configuration - провайдер настроек
- test_config.ini - настройки для тестов
- ./testdata - провайдер тестовых данных
- test_data.json

### Полезные ссылки

- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Про pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/)

### Библиотеки (!)

- pip install pytest
- pip install selenium
- pip install webdriver-manager
