FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-root --no-interaction --no-ansi

COPY src ./src


FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app/src ./src

ENV PYTHONPATH=/app/src

CMD ["uvicorn", "actividad_17.api:app", "--host", "0.0.0.0", "--port", "8000"]