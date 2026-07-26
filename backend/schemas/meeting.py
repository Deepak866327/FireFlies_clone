from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from schemas.transcript import TranscriptSegmentResponse
from schemas.action_item import ActionItemResponse
from schemas.topic import TopicResponse


class MeetingCreate(BaseModel):
    title: str
    participants: Optional[str] = None
    transcript_text: str


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    participants: Optional[str] = None


class MeetingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    participants: Optional[str] = None
    created_at: datetime
    summary: Optional[str] = None
    audio_url: Optional[str] = None
    segments: List[TranscriptSegmentResponse] = []
    action_items: List[ActionItemResponse] = []
    topics: List[TopicResponse] = []
