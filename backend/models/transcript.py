from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"), nullable=False)
    order_index = Column(Integer, nullable=False)
    speaker = Column(String, nullable=True)
    start_time = Column(Float, nullable=True)
    text = Column(Text, nullable=False)

    meeting = relationship("Meeting", back_populates="segments")
    action_items = relationship("ActionItem", back_populates="segment")
