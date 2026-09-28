"""Tag listing endpoint."""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=List[str])
def list_tags(db: Session = Depends(get_db)):
    """Return a sorted, deduplicated list of all tags in use."""
    rows = db.query(models.Entry.tags).filter(models.Entry.tags != "").all()
    tags: set = set()
    for (tags_str,) in rows:
        for tag in tags_str.split(","):
            tag = tag.strip()
            if tag:
                tags.add(tag)
    return sorted(tags)
