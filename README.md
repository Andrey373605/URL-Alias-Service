# URL Alias Service

Сервис для сокращения длинных URL до коротких уникальных ссылок с возможностью их деактивации, устаревания и сбора статистики переходов.

## Возможности

- Создание короткой ссылки для длинного URL
- Перенаправление с короткой ссылки на оригинальный URL
- Деактивация ссылок
- Устаревание ссылок (по умолчанию — 24 часа)
- Получение статистики переходов
- Swagger UI с описанием API
- Защита приватных эндпоинтов через Basic Auth

## Установка

### Требования

Перед установкой убедитесь, что на вашей машине установлены следующие инструменты:

- Python 3.11+

### Шаги для установки

1. Клонируйте репозиторий на вашу локальную машину:

   ```bash
   git clone https://github.com/Andrey373605/URL-Alias-Service
   
2. В корне проекта создайте файл .env

3. Настройте переменный окружения в файле .env
   ```bash
    SECRET_KEY=django-insecure-ваш-ключ
    DEBUG=True

    DB_HOST=db
    DB_PORT=5432

    POSTGRES_DB=name
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password

    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=adminpass

### Шаги для поднятия проекта с помощью Docker
1. Запустите Docker Desktop 
2. Находясь в корне проекта выполните команду для сборки и автоматического поднятия сервисов
   ```bash
   docker-compose up --build
   или 
   docker-compose build
   docker-compose up
3. Для остановки работы контейнеров:
   ```bash
   docker-compose down