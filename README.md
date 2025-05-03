# 📝 Mini Blog API (FastAPI)

Учебный мини-проект API блога на **FastAPI**.  
Бэкенд, работа с API, авторизация и CRUD-операции.

---

## 📁 Структура проекта

```
MiniBlogAPI/
├── app/
│   ├── main.py               
│   ├── auth_service/
│   │   ├── __init__.py  
│   │   ├── models.py
│   │   ├── routers.py
│   │   ├── schemas.py
│   │   └── security.py
│   ├── post_service/
│   │   ├── __init__.py  
│   │   ├── models.py
│   │   ├── routers.py
│   │   └── schemas.py       
│   ├── comment_service/
│   │   ├── __init__.py  
│   │   ├── models.py
│   │   ├── routers.py
│   │   └── schemas.py       
│   ├── db/
│   │   └── database.py
│   └── config.py
├── alembic/                  # Миграции Alembic
│   ├── env.py
│   ├── README.md             # Инструкция по Alembic
│   └── versions/
├── .env                      # Настройки (секреты, подключение к БД)
├── alembic.ini               # Настройки Alembic (путь к базе, пути к моделям и миграциям)
├── requirements.txt
├── .gitignore
├── .dockerignore
├── dcoker-compose.yaml
├── Dockerfile
├── entrypoint.sh             # Для ожидании доступности postgreSQL и автоматической миграции 
└── README.md
```

---

## 🚀 Запуск проекта

### 1. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate  # или .venv\Scripts\activate для Windows

pip install -r requirements.txt
```

### 2. Запуск FastAPI

```bash
uvicorn app.main:app --reload
```

После запуска:
- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc

> #### ⚙️ Для управления схемой БД используется Alembic — ([см. инструкцию.](alembic/README.md))

---

## 🔐 Аутентификация

- **Регистрация:** `POST /auth/register`
- **Вход:** `POST /auth/token` (используется `username` + `password`)
- **Обновление токена:** `POST /auth/refresh`  
  (передаётся refresh token — генерируется при логине)
- Получение токена JWT в ответ
- Добавление токена: **Authorize** в Swagger UI

> ⚠️ **Примечание:**  
> В Swagger UI можно нажать кнопку **Authorize**, чтобы ввести `access` или `refresh` токен.  
> Учти, что эндпоинт `/auth/refresh` ожидает именно **refresh токен**.  
> Если передать в него `access токен`, обновление не произойдёт.

---

## 🎮 API эндпоинты

| Метод | Маршрут               | Описание                                |
|-------|-----------------------|------------------------------------------|
| GET   | `/posts`              | Получить все посты                       |
| GET   | `/posts/{id}`         | Получить пост по ID                      |
| POST  | `/posts`              | Создать новый пост (требует токен)       |
| PUT   | `/posts/{id}`         | Обновить пост (если ты владелец)         |
| DELETE| `/posts/{id}`         | Удалить пост (если ты владелец)          |
| GET   | `/comments/post/{id}` | Получить комментарии к посту             |
| POST  | `/comments/post/{id}` | Создать комментарий к посту              |
| PUT   | `/comments/{id}`      | Обновить свой комментарий                |
| DELETE| `/comments/{id}`      | Удалить свой комментарий                 |

---

## 📦 .env файл (пример)

```
POSTGRES_DB=miniblog
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## 🐳 Docker (Запуск проекта)

```bash
# Собрать и запустить проект
docker compose up --build
```

Проект будет доступен по адресу: [http://localhost:8000](http://localhost:8000)  
Документация API: [http://localhost:8000/docs](http://localhost:8000/docs)

> ❗ При первом запуске база создастся пустой. Alembic миграции применяются автоматически.

---

## 🛠 Технологии

- **Язык:** Python 3.11+
- **Фреймворк:** FastAPI
- **ORM:** SQLAlchemy
- **Хеширование:** Passlib (bcrypt)
- **JWT:** python-jose
- **Pydantic:** для валидации
- **Swagger/OpenAPI:** автоматическая документация

---

## 📌 Планы на будущее

- [x] SQLite + SQLAlchemy
- [x] Авторизация пользователей (JWT)
- [x] Обновление access-токена через refresh-token
- [x] Swagger авторизация через JWT-токен
- [x] Ограничение доступа к CRUD только для владельца
- [x] Поддержка комментирования постов
- [x] Поддержка вложенных комментариев
- [x] Alembic для управления миграциями ([инструкция](alembic/README.md))
- [x] Подключение PostgreSQL для продакшена
- [x] Docker-файл и docker-compose
- [ ] Написание unit-тестов с pytest
- [ ] CI/CD с помощью GitHub Actions
- [ ] Документация по API с примерами (Swagger/Redoc)

---

## 👨‍💻 Автор

Создан в учебных целях с FastAPI
