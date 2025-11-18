FROM python:3.13-slim AS base

# 🛠️ Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ⚙️ Configurações do Poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
ENV PATH="/root/.local/bin:$PATH" # Adiciona Poetry ao PATH

WORKDIR /app

# 📦 Copia os arquivos de configuração do Poetry para melhor cache
COPY pyproject.toml poetry.lock* ./

# ⬇️ Instala Poetry e dependências do projeto
RUN pip install --no-cache-dir poetry \
    && poetry install --no-ansi --without dev

# 🚀 Estágio Final/Runtime
# Você pode usar 'base' se não quiser iniciar um ambiente completamente limpo,
# ou manter o 'slim' e usar 'COPY --from=base' para copiar o ambiente virtual.
# Neste caso, vamos manter simples e usar 'base' para o runtime:
FROM base 

WORKDIR /app

# 📂 Copia o restante do código
COPY . .

# 🚪 Expõe a porta
EXPOSE 8000

# 🏃 Comando de execução (com migrações)
CMD ["sh", "-c", "alembic upgrade head && uvicorn fast_api.app:app --host 0.0.0.0 --port 8000"]