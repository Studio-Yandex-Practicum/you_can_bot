# You Can Bot - telegram-бот для профориентации подростков

## Описание проекта<a name="description"></a>
Проект создан с целью помочь ребятам определить свои профессиональные интересы и склонности, а также ускорить обработку результатов тестов, что позволит им получить быстрые и точные рекомендации по выбору карьеры.

### Преимущества проекта<a name="advantages"></a>

- **Эффективность:** Telegram-бот ускоряет процесс профориентации и экономит время как ребят, так и психологов, позволяя получать результаты мгновенно.
- **Доступность:** Пользователи могут воспользоваться ботом в любое время, что сделает профориентацию более доступной и удобной.
- **Хранение результатов в базе данных**: Психологи имеют постоянный доступ к результатам тестирования пользователей, что позволяет им легко отслеживать и анализировать прогресс и потребности подростков в любое удобное время.
- **Вопросы и консультации через бота**: Подростки могут задавать вопросы психологам через бота в любое время. Психологи получают уведомления о новых запросах и могут предоставить консультацию и поддержку в Админ-панели.

### Используемый стек<a name="stack"></a>

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Python-telegram-bot][Python-telegram-bot-badge]][Python-telegram-bot-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]

### Архитектура проекта<a name="architecture"></a>

| Директория    | Описание                                                |
|---------------|---------------------------------------------------------|
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx     |
| `src/backend` | Код Django приложения                                   |
| `src/bot`     | Код бота                                                |

### Функциональные цели<a name="goals"></a>
<details>
  <summary>Нажмите, чтобы развернуть спойлер</summary>

- [ ] Доступ к тестированию только при регистрации в ЛК
- [ ] Отправка отформатированных сообщений с вопросами пользователю
- [ ] Автоматическая интерпретация результатов 8 заданий
  - [X] Задания 1-3
  - [ ] Задания 4-8
- [ ] Отправка расшифровок по профессиональным направлениям на основе результатов тестов
- [ ] Меню с возможностью просмотра списка заданий и расшифровок к ним
- [ ] Возможность через кнопку меню задать вопрос психологу
- [ ] Просмотр результата тестов в админ-панели
- [ ] Возможность ответить на вопрос подростка в админ-панели
- [ ] Уведомление психолога в telegram о том, что ему пришёл вопрос от подростка
- [ ] Тестирование API Django приложения
- [ ] Описание deploy workflow, docker образа, docker-compose, настройка nginx

</details>

### Системные требования
- Python 3.11+;
- Docker (19.03.0+) c docker compose;
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer).


## Эксплуатация и тестирование<a name="usage-and-testing"></a>

### Установка проекта локально (без docker)<a name="local-install"></a>

1. Устанавливаем инструмент для работы с виртуальным окружением и сборки пакетов **poetry**:

<details>
  <summary>Информация по poetry и его установка</summary>
<br>

**Poetry** - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>

  <details>
    <summary>Как скачать и установить?</summary>

### Установка<a name="install"></a>

1. Установите poetry следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
2. После установки перезапустите оболочку и введите команду
```SHELL
poetry --version
```
3. Если установка прошла успешно, вы получите ответ в формате
```SHELL
Poetry (version 1.2.0)
```

<table><thead><tr><td>ℹ️</td><td>
  Опционально: измените конфигурацию poetry<br>
  <code>poetry config virtualenvs.in-project true</code><br>
  Выполнение данной команды необходимо для создания виртуального окружения в папке проекта.<br>
</td></tr></thead></table>

4. Создадим виртуальное окружение нашего проекта с
помощью команды:
```SHELL
poetry install
```
Результатом выполнения команды станет создание в корне проекта папки .venv.
Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)
и pyproject.toml

Для добавления новой зависимости в окружение необходимо выполнить команду
```SHELL
poetry add <package_name>
```
_Пример использования:_
```SHELL
poetry add starlette
```
Также poetry позволяет разделять зависимости необходимые для разработки, от
основных.
Для добавления зависимости необходимой для разработки и тестирования необходимо
добавить флаг ***--group dev***
```SHELL
poetry add <package_name> --group dev
```
_Пример использования:_
```SHELL
poetry add pytest --group dev
```
  </details>
  <details>
    <summary>Порядок работы после настройки</summary>
<br>

Чтобы активировать виртуальное окружение, введите команду:
```SHELL
poetry shell
```
Существует возможность запуска скриптов и команд с помощью команды без
активации окружения:
```SHELL
poetry run <script_name>.py
```
_Примеры:_
```SHELL
poetry run python script_name>.py
poetry run pytest
poetry run black
```
Порядок работы в оболочке не меняется. Пример команды для Win:
```SHELL
python src/run_bot.py
```
Доступен стандартный метод работы с активацией окружения в терминале с помощью команд, если использовали virtualenvs.in-project true:

Для WINDOWS:
```SHELL
source .venv/Scripts/activate
```
Для UNIX:
```SHELL
source .venv/bin/activate
```
  </details>
</details>

2. Клонируем репозиторий и переходим в его директорию:

```shell
git clone https://github.com/Studio-Yandex-Practicum/you_can_bot.git && cd you_can_bot
```

3. Копируем файл **.env.example** с новым названием **.env** и заполняем его необходимыми данными:

```shell
cp .env.example .env
```
```shell
nano .env
```

4. Подготавливаем бэкенд к работе:

```shell
cd src/backend/
python manage.py migrate
```
5. Наполняем БД данными заданий:

```shell
python manage.py loaddata \
    fixtures/tasks.json \
    fixtures/task_1_data.json \
    fixtures/task_2_data.json \
    fixtures/task_3_data.json \
    fixtures/task_4_data.json \
    fixtures/task_5_data.json \
    fixtures/task_6_data.json \
    fixtures/task_7_data.json \
    fixtures/task_8_data.json
```

### Запуск проекта локально (без docker)<a name="local-run"></a>

Если нужен доступ в админскую часть для управления данными, создаем администратора:

```shell
python manage.py createsuperuser
```

Для запуска REST API бэкенда используем команду:

```shell
python manage.py runserver
```

Для запуска телеграм-бота используем команду (в отдельном терминале):
```shell
cd src/bot/
python run_bot.py
```

### Запуск тестов<a name="tests"></a>

Чтобы запустить `unittest` тестирование работы функционала проекта, нужно:
1. Для тестирования Django приложения
```SHELL
cd src/backend/
python manage.py test
```
2. Для тестирования бота
```SHELL
cd src/bot/
python -m unittest
```

### Установка и запуск в Docker-контейнерах:<a name="docker"></a>

Cкачайте и установите Docker, следуя [инструкции](https://docs.docker.com/desktop/install/windows-install/) (для
Windows; в левом меню есть возможность выбрать инструкцию для другой ОС).

1. Создайте `.env` file в папке проекта на основе `.env.example`
2. **Удалите** локальную тестовую базу (если создавали) во избежание конфликтов (optional)
3. Перейдите в папку infra:

```shell
cd infra/
```

4. Запустите следующую команду:

```shell
docker-compose up -d
```

Эта команда создаст и запустит в фоновом режиме контейнеры, необходимые для работы приложения (db, backend, bot, nginx).

5. Затем выполните следующие команды внутри контейнера `backend`

- Применение миграций
```shell
docker-compose exec backend python backend/manage.py migrate
```

- Загрузка данных заданий
```shell
docker-compose exec backend python backend/manage.py loaddata \
    backend/fixtures/tasks.json \
    backend/fixtures/task_1_data.json \
    backend/fixtures/task_2_data.json \
    backend/fixtures/task_3_data.json \
    backend/fixtures/task_4_data.json \
    backend/fixtures/task_5_data.json \
    backend/fixtures/task_6_data.json \
    backend/fixtures/task_7_data.json \
    backend/fixtures/task_8_data.json
```

- Создание супер пользователя _(optional)_

win:
```shell
docker-compose exec backend python backend/manage.py createsuperuser
```
linux:
```shell
docker compose exec -it backend python backend/manage.py createsuperuser
```

- Сбор статики
```shell
docker-compose exec backend python backend/manage.py collectstatic --no-input
```

Админка будет доступна по адресу http://127.0.0.1/admin/

## Рекомендации для разработчиков<a name="development"></a>

### Форматирование кода<a name="formatting"></a>

На проекте принято использовать black для автоформатирования кода.
https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html

В некоторых случаях форматирование словарей или последовательностей может быть неудобным для чтения, тогда можно использовать комментарии, чтобы указать участок кода, который не нужно форматировать.
```Python
# fmt: off
test_user_answers = {
    1: 'а', 2: 'а', 3: 'б', 4: 'а', 5: 'б', 6: 'а', 7: 'б',
    8: 'а', 9: 'а', 10: 'б', 11: 'а', 12: 'б', 13: 'а', 14: 'б',
    15: 'а', 16: 'а', 17: 'б', 18: 'а', 19: 'б', 20: 'а', 21: 'б',
}
# fmt: on
```

### pre-commit<a name="pre-commit"></a>

Обязательно установите _git hooks_ с помощью _pre-commit_, которые будут выполняться при `git commit`, это автоматизирует применение к вашим изменениям автоформатирование `black`, проверки `isort`, `flake8` и др.

Для этого находясь в корневой директории проекта выполните команду
```BASH
pre-commit install
```

### Работа с Poetry<a name="poetry"></a>

В этом разделе представлены наиболее часто используемые команды.

Подробнее: https://python-poetry.org/docs/cli/

Создать виртуальное окружение и установить зависимости

```
poetry install
```
Использование `--without dev` позволяет устанавливать зависимости без зависимостей группы `dev`.

Добавить зависимость в `pyproject.toml`

```
poetry add <package_name>
```

Использование `--group dev` позволяет установить зависимость, необходимую только для разработки. Это полезно для
разделения _develop_ и _prod_ зависимостей.

### Ветки<a name="branches"></a>

При создании новой ветки наследоваться от develop, не забыв спуллить себе последние изменения
Пример наименования веток:
   - `feature/send-sandwiches`
   - `fix/process-bread-not-found.`


<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge

[Python-telegram-bot-url]: https://github.com/python-telegram-bot/python-telegram-bot

[Python-telegram-bot-badge]: https://img.shields.io/badge/python--telegram--bot-4b8bbe?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
