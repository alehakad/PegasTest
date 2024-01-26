import os
import sys
import asyncpg
import asyncio
import psycopg2
import sys
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from environs import Env

env = Env()
env.read_env()


db_host, db_port, db_name, db_user, db_password = (
    env("DB_HOST"),
    env("DB_PORT"),
    env("DB_NAME"),
    env("DB_USER"),
    env("DB_PASSWORD"),
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
