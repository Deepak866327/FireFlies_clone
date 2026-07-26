from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from models import Meeting
from services import export_service

router = APIRouter(prefix="/meetings", tags=["export"])

MEDIA_TYPES = {
    "pdf": "application/pdf",
    "md": "text/markdown",
    "txt": "text/plain",
}


@router.get("/{meeting_id}/export")
def export_meeting(
    meeting_id: int,
    format: str = Query(..., pattern="^(pdf|md|txt)$"),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")

    if format == "pdf":
        content = export_service.export_pdf(meeting)
    elif format == "md":
        content = export_service.export_markdown(meeting).encode("utf-8")
    else:
        content = export_service.export_txt(meeting).encode("utf-8")

    safe_name = "".join(c for c in meeting.title if c.isalnum() or c in (" ", "-", "_")).strip()
    filename = f"{safe_name or 'meeting'}.{format}"

    return Response(
        content=content,
        media_type=MEDIA_TYPES[format],
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
