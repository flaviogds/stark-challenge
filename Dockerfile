ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PORT=80

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --upgrade pip

RUN python -m pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install  $(test virtualenv = production) --no-dev --no-interaction --no-ansi --no-root

EXPOSE 80

COPY . .

CMD exec fastapi run --host 0.0.0.0 --port=$PORT --reload ./src/main.py
