# Task Bot

## Технологии

- Python 3.12+
- PostgreSQL база данных
- Библиотеки, указанные в `requirements.txt`

## Установка и запуск

### 1. Клонирование репозитория

```sh
$ git clone <URL репозитория>
$ cd <название репозитория>
```

### 2. Установка зависимостей

```sh
$ pip install -r requirements.txt
```

### 3. Настройка конфигурации

Создайте файл `.env` в корневой папке проекта:

```
API_ID=<Ваш API ID>
API_HASH=<Ваш API HASH>
BOT_TOKEN=<Токен вашего бота>

DB_ENGINE=postgresql
DB_USERNAME=<Имя пользователя PostgreSQL>
DB_PASS=<Пароль пользователя PostgreSQL>
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<Название базы данных>
```

## 4. Настройка базы данных

### 5. Миграции базы данных

Для управления миграциями базы данных используется Alembic. Создайте файл `alembic.ini` и настройте его.
В `alembic/env.py` заполните:

```python
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import DB_URL
from models import Base

fileConfig(context.config.config_file_name)

config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

target_metadata = Base.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

Для создания и применения миграций используйте следующие команды:

```sh
$ alembic revision --autogenerate -m "initial migration"
$ alembic upgrade head
```

### 6. Запуск бота

```sh
$ python bot.py
```

### 7. Запуск с Docker

```sh
$ docker build -t task-bot .
```

```sh
$ docker run -d --name task-bot -e API_ID=<Ваш API ID> -e API_HASH=<Ваш API HASH> -e BOT_TOKEN=<Токен вашего бота> task-bot
```

## Использование

После запуска бота отправьте команду `/start` в Telegram, чтобы начать процесс регистрации. После регистрации вы сможете
создавать задачи, просматривать их и управлять ими с помощью следующих команд:

- `/start` — Регистрация и начало работы
- `/newtask` — Создать новую задачу
- `/mytasks` — Показать ваши задачи
- `/help` — Показать доступные команды


## Лицензия

```
MIT License

Copyright (c) 2024 Andrey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

