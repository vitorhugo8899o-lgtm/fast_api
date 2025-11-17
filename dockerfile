FROM python:3.13-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app


COPY pyproject.toml poetry.lock* ./


RUN pip install --no-cache-dir poetry

RUN poetry install --no-interaction --no-ansi --without dev


COPY . .


EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "fast_api.app:app", "--host", "0.0.0.0", "--port", "8000"]