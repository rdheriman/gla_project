FROM python:3.13-slim AS base

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest \
    /uv /uvx /bin/

COPY pyproject.toml uv.lock ./


# Tests / CI

FROM base AS test

RUN uv sync --frozen

COPY app ./app
COPY tests ./tests

CMD [ "uv", "run", "pytest"]


# Production

FROM base AS runtime

RUN uv sync --frozen --no-dev

COPY app ./app

CMD [ "uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]