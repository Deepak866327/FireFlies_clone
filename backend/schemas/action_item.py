from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActionItemCreate(BaseModel):
    text: str
    owner: Optional[str] = None
    segment_id: Optional[int] = None


class ActionItemUpdate(BaseModel):
    text: Optional[str] = None
    owner: Optional[str] = None
    is_done: Optional[bool] = None


class ActionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    segment_id: Optional[int] = None
    text: str
    owner: Optional[str] = None
    is_done: bool
    created_at: datetime
