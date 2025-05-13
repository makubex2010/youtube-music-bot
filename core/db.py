from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr

from config import Config


class Base(DeclarativeBase):
    """Базовый класс моделей."""

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


engine = create_async_engine(Config.DB_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False)
