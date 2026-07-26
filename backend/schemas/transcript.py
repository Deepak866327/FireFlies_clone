from typing import Optional

from pydantic import BaseModel, ConfigDict


class TranscriptSegmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_id: int
    order_index: int
    speaker: Optional[str] = None
    start_time: Optional[float] = None
    text: str
