import asyncio
# --- NOVOS IMPORTS PARA CORREÇÃO DO WINDOWS ---
import platform
import sys
# Tenta importar WindowsSelectorEventLoopPolicy para Python 3.8+ no Windows
if sys.platform == "win32":
    try:
        from asyncio.windows_events import WindowsSelectorEventLoopPolicy
        HAS_WINDOWS_SELECTOR = True
    except ImportError:
        HAS_WINDOWS_SELECTOR = False
# ---------------------------------------------

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from fast_api.database.models import mapper_registry
from fast_api.core.settings import Settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url',Settings().DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = mapper_registry.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations(): 
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online():
    # --- APLICAÇÃO DA CORREÇÃO DO EVENT LOOP PARA ALEMBIC NO WINDOWS ---
    if platform.system() == "Windows" and HAS_WINDOWS_SELECTOR:
        # Usa a política correta que resolve o erro do ProactorEventLoop no Python 3.13
        asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    # ------------------------------------------------------------------
    
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()