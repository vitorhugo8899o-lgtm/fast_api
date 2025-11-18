FROM python:3.13-slim AS base


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
ENV PATH="/root/.local/bin:$PATH" 

WORKDIR /app

COPY pyproject.toml poetry.lock* ./


RUN pip install --no-cache-dir poetry \
    && poetry install --no-ansi --without dev


FROM base 

WORKDIR /app


COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn fast_api.app:app --host 0.0.0.0 --port 8000"]