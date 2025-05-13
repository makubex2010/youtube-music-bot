from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.db import Base


class User(Base):
    """Модель Пользователя."""

    username = Column(String(64), nullable=True)
    audios = relationship(
        "Audio", back_populates="user",
        cascade="all, delete-orphan", lazy="selectin"
    )
