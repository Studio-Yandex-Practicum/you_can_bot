FROM python:3.11-slim as requirements

WORKDIR ./app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./

RUN poetry export --without-hashes --without=dev > requirements.txt

FROM python:3.11-slim as base

COPY --from=requirements ./app ./app

WORKDIR ./app
RUN pip install -r ./requirements.txt --no-cache-dir
RUN pip install python-dotenv

COPY ./src ./
