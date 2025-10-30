import os
import sys
import asyncio
from alembic import context
from sqlalchemy import pool
from app.database.database import Base
from logging.config import fileConfig
from sqlalchemy.engine import Connection
from app.database.models.building import Building
from app.database.models.activity import Activity
from app.config.config import DATABASE_URL, \
     DB_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from sqlalchemy.ext.asyncio import async_engine_from_config
from app.database.models.company import Company, CompanyPhone


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_database_url():
    database_url = DATABASE_URL
    if database_url:
        return database_url
    return f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        compare_type=True,         
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()