# 📦 Alembic — миграции базы данных

---

## 🔧 Установка

```bash
pip install -r requirements.txt
```

---

## ⚙️ Настройка Alembic

Уже всё настроено:
- Файл `alembic.ini` указывает на директорию миграций
- В `env.py` подключена `Base.metadata` из SQLAlchemy
- Поддерживается автогенерация миграций и автоформатирование с помощью `black`

> ⚠️ Убедись, что переменная `DATABASE_URL` настроена в `.env`,  
> а в `alembic.ini` корректно указан путь:  
> `sqlalchemy.url = ${DATABASE_URL}`

В `env.py` указано:
```python
from app.db.database import Base  # или из app.auth_service.models / post_service.models
target_metadata = Base.metadata
```
Это позволяет Alembic отслеживать изменения моделей в проекте.

---

## 🚀 Использование Alembic

### 📄 Создать миграцию (автоматически)

```bash
alembic revision --autogenerate -m "описание"
```

> 💡 Можно без `-m`, тогда имя будет создано по шаблону из `alembic.ini`:
> `2025_04_23_1127-3fdb8df82a91_initial_full_migration.py`

### ⬆ Применить миграции

```bash
alembic upgrade head
```

### ⬇ Откатить одну миграцию

```bash
alembic downgrade -1
```

### 🧹 Сбросить БД (например, SQLite)

```bash
rm blog.db
alembic upgrade head
```

---

## 🛠 Первая миграция (если вручную)

Если автогенерация не требуется, можно создать пустую миграцию и вписать изменения вручную:

```bash
alembic revision -m "initial"
```

Далее в созданном файле указываются изменения с помощью `op.create_table`, `op.add_column` и т.д.

---

## 🛠 Makefile (опционально)

Если хочешь, можешь использовать `Makefile`:

```makefile
migrate:
	alembic revision --autogenerate -m "new migration"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

reset-db:
	rm blog.db
	alembic upgrade head
```

Теперь удобно вызывать команды:

```bash
make migrate
make upgrade
make reset-db
```

---

## 🧪 Тестирование (опционально)

Можно создать отдельную SQLite БД для тестов и применять миграции на неё в `pytest`.

---

## ❓ Зачем нужны миграции?

Чтобы безопасно и удобно **менять структуру БД**:
- создаются/удаляются таблицы
- добавляются/переименовываются поля
- изменения фиксируются в истории
- можно повторить их на проде, откатить назад, протестировать

Незаменимы при командной разработке или CI/CD.