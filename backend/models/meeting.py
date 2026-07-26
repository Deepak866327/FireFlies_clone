from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    participants = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    summary = Column(Text, nullable=True)
    audio_url = Column(String, nullable=True)

    segments = relationship(
        "TranscriptSegment", back_populates="meeting", cascade="all, delete-orphan"
    )
    action_items = relationship(
        "ActionItem", back_populates="meeting", cascade="all, delete-orphan"
    )
    topics = relationship(
        "Topic", back_populates="meeting", cascade="all, delete-orphan"
    )
