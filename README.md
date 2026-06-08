# job-monitor-service

## Описание

Job Monitor Service — сервис для мониторинга вакансий из источника RemoteOK с возможностью автоматического 
отслеживания новых публикаций, фильтрации данных и отправки уведомлений пользователям в телеграмм бот.

Сервис предназначен для автоматизации поиска вакансий и оперативного информирования о новых предложениях,
соответствующих заданным критериям.

## Основные возможности

* Мониторинг вакансий из RemoteOK.
* Сбор и обработка данных о вакансиях.
* Фильтрация по ключевым словам.
* Хранение вакансий в базе данных.
* REST API для получения вакансии.
* Автоматическое обновление информации по расписанию.
* Telegram-бот для взаимодействия с пользователями.
* Отправка уведомлений о новых вакансиях по подписке в телеграмм бот.

## Технологии

* Python 3.13
* FastAPI
* SQLAlchemy
* Alembic
* PostgreSQL
* Docker
* APSCheduler
* Aiogram

## Структура проекта

```text
.
├── alembic/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── subscription/
│   ├── user/
│   ├── vacancies/
│   ├── web/
│   └── main.py
├── telegram_bot/
│   ├── bot.py
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## Запуск через Docker Compose

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd job-monitor-service
```

### 2. Настройка переменных окружения

Создайте файл `.env` и заполните необходимые параметры.

### 3. Запуск

```bash
docker compose up -d --build
```

Проверка запущенных контейнеров:

```bash
docker compose ps
```

## Локальный запуск

Создание виртуального окружения:

```bash
python -m venv venv
```

Активация:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

Запуск приложения:

```bash
uvicorn app.main:app --reload
```

## API Documentation

После запуска документация доступна по адресам:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

## Разработка

Запуск тестов:

```bash
pytest
```
