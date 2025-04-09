
# 📝 Mini Blog API (FastAPI)

Учебный мини-проект API блога на **FastAPI**.  
Подходит для новичков, изучающих бэкенд, работу с API, авторизацию и CRUD-операции.

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
│   ├── db/
│   │   └── database.py
│   └── config.py
├── .env                      # Настройки (секреты, подключение к БД)
├── requirements.txt
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

---

## 🔐 Аутентификация

- Регистрация: `POST /auth/register`
- Вход: `POST /auth/token` (используется `username` + `password`)
- Получение токена JWT в ответ
- Добавление токена: **Authorize** в Swagger UI

---

## 🎮 API эндпоинты

| Метод | Маршрут           | Описание                                |
|-------|-------------------|------------------------------------------|
| GET   | `/posts`          | Получить все посты                       |
| GET   | `/posts/{id}`     | Получить пост по ID                      |
| POST  | `/posts`          | Создать новый пост (требует токен)       |
| PUT   | `/posts/{id}`     | Обновить пост (если ты владелец)         |
| DELETE| `/posts/{id}`     | Удалить пост (если ты владелец)          |

---

## 📦 .env файл (пример)

```
DATABASE_URL=sqlite:///./blog.db
SECRET_KEY=секретный_ключ
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

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
- [ ] Docker-файл для деплоя
- [ ] Подключение PostgreSQL для продакшена
- [ ] Написание unit-тестов с pytest
- [ ] CI/CD с помощью GitHub Actions
- [ ] Поддержка комментирования постов
- [ ] Ограничение доступа к CRUD только для владельца
- [ ] Документация по API с примерами (Swagger/Redoc)
- [ ] Swagger авторизация через JWT-токен

---

## 👨‍💻 Автор

Создан в учебных целях с любовью к коду и FastAPI ❤️  
Расширяй, улучшай и экспериментируй!
