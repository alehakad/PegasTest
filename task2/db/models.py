from sqlalchemy import (
    Column,
    String,
    BigInteger,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(BigInteger, unique=True, server_default=text("NULL"))
    user_name = Column(String(300))
