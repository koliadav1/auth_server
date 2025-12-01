# Система авторизации и аутентификации

Система авторизации и аутентификации с гибкой системой прав доступа, написанная на FastAPI и SQLAlchemy

## Оглавление

- [Возможности](#возможности)
- [Технологии](#технологии)
- [API Документация](#api-документация)
- [Структура проекта](#структура-проекта)
- [Настройка окружения](#настройка-окружения)
- [Запуск проекта](#запуск-проекта)
- [Миграции](#миграции)
- [Тесты](#тесты)
- [Структура управления ограничениями доступа](#структура-управления-ограничениями-доступа)

---

## Возможности

### Аутентификация
- Регистрация пользователей с подтверждением пароля
- Логин/Логаут с JWT токенами
- Refresh токены для продления сессии
- Мягкое удаление аккаунтов 
- Обновление профиля пользователя

### Авторизация
- Ролевая модель (администратор, менеджер, пользователь, гость)
- Матрица прав доступа к бизнес-объектам
- Гибкая система разрешений (read, create, update, delete)
- Разграничение прав на свои/все объекты
- Admin API для управления правами

### Бизнес-объекты (Mock)
- Пользователи
- Товары
- Заказы
- Магазины

## Технологии

- **Backend:** FastAPI, SQLAlchemy, Pydantic, Asyncio
- **База данных:** PostgreSQL
- **Аутентификация:** JWT, bcrypt
- **Документация API:** Swagger
- **Миграции:** Alembic
- **Тестирование:** PyTest
- **Контейнеризация:** Docker, docker-compose

---

## API Документация

После запуска проекта полная документация API доступна через Swagger UI:
- **Swagger UI:** http://localhost:8000/docs

Документация включает все эндпоинты, схемы запросов/ответов и возможность тестирования API.

---

## Структура проекта

```
app/
  core/
    dependencies.py
    security.py
  migrations/
  routers/
  models/
  schemas/
  services/
  config.py
  database.py
  main.py
tests/
  test_routers/
  test_services/
  conftest.py
  test_utils.py
scripts/
  start.sh
alembic.ini
docker-compose.yml
Dockerfile
README.md
requirements.txt
.env.example
```

## Настройка окружения

Перед первым запуском создайте файл `.env` в корне проекта либо воспользуйтесь `.env.example`:

```env
# База данных
DB_HOST=postgres
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-user-name
DB_PASSWORD=your-db-password

# JWT
ACCESS_TOKEN_SECRET_KEY=your-secret-access-key
REFRESH_TOKEN_SECRET_KEY=your-secret-refresh-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=expiration-time(minutes)
REFRESH_TOKEN_EXPIRE_DAYS=expiration-time(days)

```
Все переменные обязательны для работы приложения.# Система авторизации и аутентификации

Система авторизации и аутентификации с гибкой системой прав доступа, написанная на FastAPI и SQLAlchemy

## Оглавление

- [Возможности](#возможности)
- [Технологии](#технологии)
- [API Документация](#api-документация)
- [Структура проекта](#структура-проекта)
- [Настройка окружения](#настройка-окружения)
- [Запуск проекта](#запуск-проекта)
- [Миграции](#миграции)
- [Тесты](#тесты)
- [Структура управления ограничениями доступа](#структура-управления-ограничениями-доступа)

---

## Возможности

### Аутентификация
- Регистрация пользователей с подтверждением пароля
- Логин/Логаут с JWT токенами
- Refresh токены для продления сессии
- Мягкое удаление аккаунтов 
- Обновление профиля пользователя

### Авторизация
- Ролевая модель (администратор, менеджер, пользователь, гость)
- Матрица прав доступа к бизнес-объектам
- Гибкая система разрешений (read, create, update, delete)
- Разграничение прав на свои/все объекты
- Admin API для управления правами

### Бизнес-объекты (Mock)
- Пользователи
- Товары
- Заказы
- Магазины

## Технологии

- **Backend:** FastAPI, SQLAlchemy, Pydantic, Asyncio
- **База данных:** PostgreSQL
- **Аутентификация:** JWT, bcrypt
- **Документация API:** Swagger
- **Миграции:** Alembic
- **Тестирование:** PyTest
- **Контейнеризация:** Docker, docker-compose

---

## API Документация

После запуска проекта полная документация API доступна через Swagger UI:
- **Swagger UI:** http://localhost:8000/docs

Документация включает все эндпоинты, схемы запросов/ответов и возможность тестирования API.

---

## Структура проекта

```
app/
  core/
    dependencies.py
    security.py
  migrations/
  routers/
  models/
  schemas/
  services/
  config.py
  database.py
  main.py
tests/
  test_routers/
  test_services/
  conftest.py
  test_utils.py
scripts/
  start.sh
alembic.ini
docker-compose.yml
Dockerfile
README.md
requirements.txt
.env.example
```

## Настройка окружения

Перед первым запуском создайте файл `.env` в корне проекта либо воспользуйтесь `.env.example`:

```env
# База данных
DB_HOST=postgres
DB_PORT=5432
DB_NAME=your-db-name
DB_USER=your-user-name
DB_PASSWORD=your-db-password

# JWT
ACCESS_TOKEN_SECRET_KEY=your-secret-access-key
REFRESH_TOKEN_SECRET_KEY=your-secret-refresh-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=expiration-time(minutes)
REFRESH_TOKEN_EXPIRE_DAYS=expiration-time(days)

```
Все переменные обязательны для работы приложения.

---

## Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/koliadav1/auth-server.git
cd auth-server
```

### 2. Настроить окружение
- Создайте .env файл (см. раздел "Настройка окружения")

### 3. Запустить контейнеры
```bash
docker-compose up --build
```

### 4. Приложение будет доступно по адресу:
- API: http://localhost:8000
- Swagger-документация: http://localhost:8000/docs

### 5. Тестовые данные

Для тестирования работы приложения были добавлены данные, включая тестовых пользователей всех ролей:
#### Админ
- Логин: admin@example.com
- Пароль: 123
#### Менеджер
- Логин: manager@example.com
- Пароль: 456
#### Пользователь
- Логин: user@example.com
- Пароль: 789
#### Гость
- Логин: guest@example.com
- Пароль: 1234

---

## Миграции

Создание новой миграции:  
```bash
docker-compose exec web alembic revision --autogenerate -m "migration name"
```

Применение миграций:  
```bash
docker-compose exec web alembic upgrade head
```

---

## Тесты

Запуск тестов: 
```bash
docker-compose exec web pytest
```

---

## Структура управления ограничениями доступа

Система реализует ролевую модель с матрицей прав доступа, где права задаются не на уровне отдельных пользователей, а на уровне ролей, что обеспечивает простоту управления. Кроме того, имеется возможность добавлять новые роли и бизнес-элементы, что повышает масштабируемость системы.

### Матрица действий и прав
- read - просмотр собственных объектов
- read_all - просмотр всех объектов системы
- create - создание новых объектов
- update - изменение собственных объектов
- update_all - изменение любых объектов
- delete - удаление собственных объектов
- delete_all - удаление любых объектов


---

## Запуск проекта

### 1. Клонировать репозиторий
```bash
git clone https://github.com/koliadav1/auth-server.git
cd auth-server
```

### 2. Настроить окружение
- Создайте .env файл (см. раздел "Настройка окружения")

### 3. Запустить контейнеры
```bash
docker-compose up --build
```

### 4. Приложение будет доступно по адресу:
- API: http://localhost:8000
- Swagger-документация: http://localhost:8000/docs

### 5. Тестовые данные

Для тестирования работы приложения были добавлены данные, включая тестовых пользователей всех ролей:
Админ
- Логин: admin@example.com
- Пароль: 123


---

## Миграции

Создание новой миграции:  
```bash
docker-compose exec web alembic revision --autogenerate -m "migration name"
```

Применение миграций:  
```bash
docker-compose exec web alembic upgrade head
```

---

## Тесты

Запуск тестов: 
```bash
docker-compose exec web pytest
```

---

## Структура управления ограничениями доступа

Система реализует ролевую модель с матрицей прав доступа, где права задаются не на уровне отдельных пользователей, а на уровне ролей, что обеспечивает простоту управления. Кроме того, имеется возможность добавлять новые роли и бизнес-элементы, что повышает масштабируемость системы.

### Матрица действий и прав
- read - просмотр собственных объектов
- read_all - просмотр всех объектов системы
- create - создание новых объектов
- update - изменение собственных объектов
- update_all - изменение любых объектов
- delete - удаление собственных объектов
- delete_all - удаление любых объектов
