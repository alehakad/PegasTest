from sqlalchemy import (
    Column,
    String,
    BigInteger,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from .conn import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, server_default=text("NULL"))
    user_name = Column(String(300))


Base.metadata.create_all(engine)
