from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models import ActionItem

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.patch("/{action_item_id}", response_model=schemas.ActionItemResponse)
def update_action_item(
    action_item_id: int, payload: schemas.ActionItemUpdate, db: Session = Depends(get_db)
):
    action_item = db.query(ActionItem).filter(ActionItem.id == action_item_id).first()
    if not action_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found")

    if payload.text is not None:
        action_item.text = payload.text
    if payload.owner is not None:
        action_item.owner = payload.owner
    if payload.is_done is not None:
        action_item.is_done = payload.is_done

    db.commit()
    db.refresh(action_item)
    return action_item
