import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.core.database import Base, engine  # O'zgartirilgan engine

# Alembic konfiguratsiya faylini yuklash
config = context.config

# Log sozlamalarini o'rnatish
fileConfig(config.config_file_name)

# Metadatalarni olish
target_metadata = Base.metadata

def run_migrations_online():
    # Ulanishni sinxron qilish
    connectable = engine  # Asinxron emas, engine sinxron bo'ladi
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline():
    # Offline rejimida migratsiyani bajarish
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# Alembic onlayn yoki oflayn rejimida ishlashini aniqlash
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
