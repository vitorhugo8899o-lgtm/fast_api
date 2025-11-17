FROM python:3.13-slim


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV POETRY_VIRTUALENVS_CREATE=false

FROM python:3.13-slim

# Atualiza e instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configurações do Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1

WORKDIR /app

# Copia apenas os arquivos do Poetry primeiro (melhora cache)
COPY pyproject.toml poetry.lock* ./

# Instala Poetry
RUN pip install --no-cache-dir poetry

# Instala dependências do projeto
RUN poetry install --no-ansi --without dev

# Agora copia o restante do código
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "fast_api.app:app", "--host", "0.0.0.0", "--port", "8000"]