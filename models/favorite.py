from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from core.db import Base


class Audio(Base):
    """Модель избранного аудио."""

    title = Column(String(64), nullable=True)
    message_id = Column(Integer, nullable=True)
    user = relationship("User", back_populates="audios")
    user_id = Column(Integer, ForeignKey("user.id"))
    forwarded_message_id = Column(Integer, nullable=True)

    def __str__(self) -> str:
        return f"{self.title}"

    def __repr__(self) -> str:
        return f"{self.title}"
