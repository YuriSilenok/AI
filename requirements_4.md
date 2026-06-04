## 🔹 Требования на оценку 4 (исключая оценку 3)

### 1. Общие требования
- Реализовать **REST API** с использованием **FastAPI**.
- Все данные должны быть получены из БД и записаны в БД с использованием **Peewee**.
- Допускается хранение временных данных в **сессиях**.
- Реализована **валидация данных** (через Pydantic + typing).
- Вся реализация API, включая **схемы и логику**, должна находиться **внутри `service.py`**.

---

## 🔹 Содержимое файла `service.py` (оценка 4)

### 1. Импорты
```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import peewee
```

### 2. Описание API (документация)
- Должны быть перечислены **точки входа** (endpoints)
- Для каждой точки указаны:
  - HTTP-метод (GET, POST, PUT, DELETE)
  - Параметры запроса (path, query, body)
  - Назначение
  - Пример ответа (в комментариях или докстрингах)

### 3. Схемы данных (Pydantic)
- Валидация входных и выходных данных
- Обязательность полей
- Типы данных
- Ограничения (например, `Field(..., min_length=1, max_length=100)`)
- Значения по умолчанию (если есть)

Пример:
```python
class EntityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
```

### 4. Логика работы с БД (Peewee)
- Модели должны быть описаны (или импортированы из `models.py`, но сама логика работы с ними — внутри `service.py`)
- Выполнение CRUD-операций:
  - создание
  - изменение по ID
  - удаление (логическое — `is_active = False`)
  - получение по ID
  - получение списка с фильтрацией

### 5. Реализация эндпоинтов FastAPI

#### Обязательные эндпоинты для каждой сущности (как в ТЗ на оценку 3, но реализованные через REST API):

#### ✅ **Создание сущности**
- Метод: `POST`
- Параметры: JSON-тело (валидируется через Pydantic)
- Возвращает: созданный объект с ID

#### ✅ **Изменение сущности по ID**
- Метод: `PUT` или `PATCH`
- Параметры: `id` в пути, JSON-тело с изменениями
- Возвращает: обновлённый объект

#### ✅ **Удаление сущности по ID**
- Метод: `DELETE`
- Параметры: `id` в пути
- Возвращает: `{"success": true}` или `{"success": false}`
- Реализация: логическое удаление (`is_active = False`)

#### ✅ **Получить сущность по ID**
- Метод: `GET`
- Параметры: `id` в пути
- Возвращает: объект сущности

#### ✅ **Получить список сущностей по параметрам**
- Метод: `GET`
- Параметры: query-параметры (например, `?name=...`)
- Возвращает: список объектов

### 6. Валидация данных
- На уровне Pydantic (типы, обязательность, длина, формат)
- На уровне бизнес-логики (например, проверка уникальности, существования связанных записей)

### 7. Работа с БД через Peewee
- Получение данных: `Entity.get()`, `Entity.select()`
- Вставка: `Entity.create()`
- Обновление: `entity.save()`
- Удаление: `entity.is_active = False; entity.save()`

---

## 🔹 Чего НЕ должно быть в `service.py` (оценка 3)
- Моделей БД (они в `models.py`)
- Инициализации БД (она в `models.py`)
- ER-диаграммы
- Описания API в `doc.md`
- Требований к UI (это оценка 5)

---

## 🔹 Структура `service.py` (оценка 4)

```python
# service.py

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from models import Entity, db  # если models.py существует

app = FastAPI()

# ----- СХЕМЫ (Pydantic) -----
class EntityCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    ...

class EntityResponse(BaseModel):
    id: int
    name: str
    ...

# ----- ЛОГИКА (Peewee) -----
def get_entity_by_id(entity_id: int):
    ...

# ----- ЭНДПОИНТЫ -----
@app.post("/entities/", response_model=EntityResponse)
def create_entity(data: EntityCreate):
    ...

@app.put("/entities/{entity_id}", response_model=EntityResponse)
def update_entity(entity_id: int, data: EntityCreate):
    ...

@app.delete("/entities/{entity_id}")
def delete_entity(entity_id: int):
    ...

@app.get("/entities/{entity_id}", response_model=EntityResponse)
def get_entity(entity_id: int):
    ...

@app.get("/entities/", response_model=List[EntityResponse])
def list_entities(name: Optional[str] = Query(None)):
    ...
```

---

## 🔹 Итог: на оценку 4 в `service.py` должно быть
- ✅ Полное REST API на FastAPI
- ✅ Валидация через Pydantic
- ✅ Логика работы с БД на Peewee
- ✅ Эндпоинты: CRUD + список с фильтрацией
- ❌ Без UI (это оценка 5)
- ❌ Без инициализации БД (это оценка 3/models.py)

## Правила для ИИ при проверке работы

- Код в файле models.py должен соответствовать версии python 3.8
- Тебе как нейросети разрешено отвечать только списком замечаний или написать "Замечаний нет".
- Ты как нейросеть обязан процитировать, какье требование было нарушено, при написании замечания.
- Не проверяй опечатки связанные с кавычками " или '
- Считай нормальным отсутсвие проверки уникальности поля на уровни API.
- Считай нормальным что обновление поля updated_at не реализоно на уровне API.
