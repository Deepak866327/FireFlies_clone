import json
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import Meeting, TranscriptSegment
from services import meeting_service

router = APIRouter(prefix="/meetings", tags=["meetings"])

DATE_FILTERS = {"today", "7d", "30d", "year"}


@router.get("", response_model=List[schemas.MeetingResponse])
def list_meetings(
    search: Optional[str] = Query(None),
    date_filter: Optional[str] = Query(None),
    sort: Optional[str] = Query("newest"),
    db: Session = Depends(get_db),
):
    query = db.query(Meeting)

    if search:
        like = f"%{search}%"
        matching_meeting_ids = db.query(TranscriptSegment.meeting_id).filter(
            TranscriptSegment.text.ilike(like)
        )
        query = query.filter(
            or_(
                Meeting.title.ilike(like),
                Meeting.participants.ilike(like),
                Meeting.id.in_(matching_meeting_ids),
            )
        )

    if date_filter in DATE_FILTERS:
        now = datetime.utcnow()
        if date_filter == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif date_filter == "7d":
            start = now - timedelta(days=7)
        elif date_filter == "30d":
            start = now - timedelta(days=30)
        else:  # "year"
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(Meeting.created_at >= start)

    if sort == "oldest":
        query = query.order_by(Meeting.created_at.asc())
    elif sort == "az":
        query = query.order_by(func.lower(Meeting.title).asc())
    elif sort == "za":
        query = query.order_by(func.lower(Meeting.title).desc())
    else:
        query = query.order_by(Meeting.created_at.desc())

    return query.all()


@router.get("/{meeting_id}", response_model=schemas.MeetingResponse)
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
    return meeting


@router.get("/{meeting_id}/transcript", response_model=List[schemas.TranscriptSegmentResponse])
def search_transcript(
    meeting_id: int, search: Optional[str] = Query(None), db: Session = Depends(get_db)
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    query = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting_id)
    if search:
        query = query.filter(TranscriptSegment.text.ilike(f"%{search}%"))

    return query.order_by(TranscriptSegment.order_index).all()


@router.post("", response_model=schemas.MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(
    title: str = Form(...),
    participants: Optional[str] = Form(None),
    transcript_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    if not transcript_text and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide transcript_text or upload a .txt/.json transcript file",
        )

    if file:
        if not file.filename.endswith((".txt", ".json")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .txt or .json transcript files are supported",
            )
        raw_bytes = file.file.read()
        if file.filename.endswith(".json"):
            try:
                payload = json.loads(raw_bytes)
            except json.JSONDecodeError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid JSON transcript file"
                )
            transcript_text = meeting_service.transcript_text_from_json(payload)
        else:
            transcript_text = raw_bytes.decode("utf-8")

    if not transcript_text or not transcript_text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Transcript is empty")

    return meeting_service.create_meeting(
        db, title=title, participants=participants, transcript_text=transcript_text
    )


@router.put("/{meeting_id}", response_model=schemas.MeetingResponse)
def update_meeting(meeting_id: int, payload: schemas.MeetingUpdate, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    if payload.title is not None:
        meeting.title = payload.title
    if payload.participants is not None:
        meeting.participants = payload.participants

    db.commit()
    db.refresh(meeting)
    return meeting


@router.delete("/{meeting_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    db.delete(meeting)
    db.commit()
