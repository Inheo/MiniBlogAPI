# 📝 Mini Blog API (FastAPI)

Учебный мини-проект API блога на **FastAPI**.  
Подходит для новичков, изучающих бэкенд, работу с API, роутинг и CRUD-операции.

---

## 📁 Структура проекта

```
Test/
├── app/
│   ├── main.py                # Точка входа FastAPI
│   ├── routers/
│   │   └── posts.py           # CRUD-маршруты для постов
│   ├── models/
│   │   └── post.py            # Pydantic-модель Post
│   └── db/
│       └── fake_db.py         # Фейковая БД
├── requirements.txt
└── README.md
```

---

## 🚀 Запуск проекта

### 1. Установка зависимостей

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# или source .venv/bin/activate для macOS/Linux

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

## 🎮 API эндпоинты

| Метод | Маршрут           | Описание              |
|-------|-------------------|------------------------|
| GET   | `/posts`          | Получить все посты     |
| GET   | `/posts/{id}`     | Получить пост по ID    |
| POST  | `/posts`          | Создать новый пост     |
| PUT   | `/posts/{id}`     | Обновить пост          |
| DELETE| `/posts/{id}`     | Удалить пост           |

---

## 🧪 Пример запроса (POST)

```json
POST /posts
Content-Type: application/json

{
  "id": 1,
  "title": "Мой первый пост",
  "content": "Это тестовое сообщение!"
}
```

---

## 🛠 Технологии

- **Backend:** Python, FastAPI
- **Документация:** Swagger UI (автоматически)
- **База данных:** временно фейковая (в памяти)

---

## 📌 Планы на будущее

- [ ] SQLite + SQLAlchemy
- [ ] Авторизация пользователей (JWT)
- [ ] Docker-файл для деплоя

---

## 👨‍💻 Автор

Создан в учебных целях с урбечом❤️ и FastAPI  
Feel free to fork, play, and expand!
