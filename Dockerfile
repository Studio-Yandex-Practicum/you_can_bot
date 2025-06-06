FROM python:3.11-slim AS requirements

WORKDIR /app

RUN pip install poetry==2.1.2

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-ansi --no-root


FROM python:3.11-slim

WORKDIR /app

COPY --from=requirements /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=requirements /usr/local/bin /usr/local/bin

COPY ./src ./
