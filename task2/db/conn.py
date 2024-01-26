import os
import sys
import asyncpg
import asyncio
import psycopg2
import sys
from sqlalchemy import event
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker

db_host, db_port, db_name, db_user, db_password = (
    config.db.db_host,
    config.db.db_port,
    config.db.db_name,
    config.db.db_user,
    config.db.db_password,
)

engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
async_engine = create_async_engine(
    f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

Session = sessionmaker(bind=engine)
AsyncSession = async_sessionmaker(
    bind=async_engine, sync_session_class=Session
)  # sync_session_class-
