from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Meeting
from services.chat_service import ask_about_meeting
from services.llm import (
    LLMConfigError,
    LLMError,
    LLMRateLimitError,
    LLMRequestError,
    LLMTimeoutError,
    UnsupportedProviderError,
)

router = APIRouter(prefix="/meetings", tags=["chat"])


@router.post("/{meeting_id}/chat", response_model=schemas.ChatResponse)
def chat_about_meeting(
    meeting_id: int, payload: schemas.ChatRequest, db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    history = [message.model_dump() for message in (payload.history or [])]

    try:
        answer = ask_about_meeting(meeting, payload.provider, payload.question, history)
    except UnsupportedProviderError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except LLMConfigError as exc:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
    except LLMRateLimitError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc))
    except LLMTimeoutError as exc:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(exc))
    except (LLMRequestError, LLMError) as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))

    return schemas.ChatResponse(answer=answer, provider=payload.provider)
