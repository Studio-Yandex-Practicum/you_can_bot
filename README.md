# you_can_bot
Чат-бот по профориентации
## Poetry (инструмент для работы с виртуальным окружением и сборки пакетов)<a id="poetry"></a>:

Poetry - это инструмент для управления зависимостями и виртуальными окружениями, также может использоваться для сборки пакетов. В этом проекте Poetry необходим для дальнейшей разработки приложения, его установка <b>обязательна</b>.<br>

<details>
 <summary>
 Как скачать и установить?
 </summary>

### Установка:

Установите poetry следуя [инструкции с официального сайта](https://python-poetry.org/docs/#installation).
<details>
 <summary>
 Команды для установки:
 </summary>
Для UNIX-систем и Bash on Windows вводим в консоль следующую команду:

> *curl -sSL https://install.python-poetry.org | python -*

Для WINDOWS PowerShell:

> *(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -*
</details>
<br>
После установки перезапустите оболочку и введите команду

> poetry --version

Если установка прошла успешно, вы получите ответ в формате

> Poetry (version 1.2.0)

Для дальнейшей работы введите команду:

> poetry config virtualenvs.in-project true

Выполнение данной команды необходимо для создания виртуального окружения в
папке проекта.

После предыдущей команды создадим виртуальное окружение нашего проекта с
помощью команды:

> poetry install

Результатом выполнения команды станет создание в корне проекта папки .venv.
Зависимости для создания окружения берутся из файлов poetry.lock (приоритетнее)
и pyproject.toml

Для добавления новой зависимости в окружение необходимо выполнить команду

> poetry add <package_name>

_Пример использования:_

> poetry add starlette

Также poetry позволяет разделять зависимости необходимые для разработки, от
основных.
Для добавления зависимости необходимой для разработки и тестирования необходимо
добавить флаг ***--group dev***

> poetry add <package_name> --group dev

_Пример использования:_

> poetry add pytest --group dev

</details>

<details>
 <summary>
 Порядок работы после настройки
 </summary>

<br>

Чтобы активировать виртуальное окружение, введите команду:

> poetry shell

Существует возможность запуска скриптов и команд с помощью команды без
активации окружения:

> poetry run <script_name>.py

_Примеры:_

> poetry run python script_name>.py
>
> poetry run pytest
>
> poetry run black

Порядок работы в оболочке не меняется. Пример команды для Win:

> python src\run_bot.py

Доступен стандартный метод работы с активацией окружения в терминале с помощью команд:

Для WINDOWS:

> source .venv/Scripts/activate

Для UNIX:

> source .venv/bin/activate

</details>

## Запуск проекта локально <a id="run-local"></a>
<details>
 <summary>
 Запуск проекта локально
 </summary>
<br>

1. Создать и заполнить `.env` по образцу `/.env.example`

2. Запустить бота командой

```BASH
python src/bot/run_bot.py
```

</details>
