"""Knowledge-entry CRUD and search endpoints."""
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/entries", tags=["entries"])


def _tags_to_str(tags: List[str]) -> str:
    return ",".join(t.strip() for t in tags if t.strip())


def _str_to_tags(tags_str: str) -> List[str]:
    return [t for t in tags_str.split(",") if t] if tags_str else []


def _entry_to_out(entry: models.Entry) -> schemas.EntryOut:
    return schemas.EntryOut(
        id=entry.id,
        title=entry.title,
        content=entry.content,
        tags=_str_to_tags(entry.tags),
        category=entry.category,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
    )


def _snapshot(db: Session, entry: models.Entry) -> None:
    """Persist current state of an entry as a new version."""
    version = models.EntryVersion(
        entry_id=entry.id,
        title=entry.title,
        content=entry.content,
        tags=entry.tags,
        category=entry.category,
    )
    db.add(version)


@router.get("", response_model=schemas.EntryListOut)
def list_entries(
    q: Optional[str] = Query(None, description="Full-text search query"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    category: Optional[str] = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    query = db.query(models.Entry)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(models.Entry.title.ilike(like), models.Entry.content.ilike(like))
        )
    if tag:
        query = query.filter(models.Entry.tags.ilike(f"%{tag}%"))
    if category:
        query = query.filter(models.Entry.category == category)

    total = query.count()
    items = query.order_by(models.Entry.updated_at.desc()).offset(skip).limit(limit).all()
    return schemas.EntryListOut(total=total, items=[_entry_to_out(e) for e in items])


@router.post("", response_model=schemas.EntryOut, status_code=status.HTTP_201_CREATED)
def create_entry(body: schemas.EntryCreate, db: Session = Depends(get_db)):
    entry = models.Entry(
        title=body.title,
        content=body.content,
        tags=_tags_to_str(body.tags),
        category=body.category,
    )
    db.add(entry)
    db.flush()  # populate entry.id before snapshot
    _snapshot(db, entry)
    db.commit()
    db.refresh(entry)
    return _entry_to_out(entry)


@router.get("/{entry_id}", response_model=schemas.EntryOut)
def get_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return _entry_to_out(entry)


@router.put("/{entry_id}", response_model=schemas.EntryOut)
def update_entry(entry_id: str, body: schemas.EntryUpdate, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    if body.title is not None:
        entry.title = body.title
    if body.content is not None:
        entry.content = body.content
    if body.tags is not None:
        entry.tags = _tags_to_str(body.tags)
    if body.category is not None:
        entry.category = body.category

    entry.updated_at = datetime.now(timezone.utc)
    _snapshot(db, entry)
    db.commit()
    db.refresh(entry)
    return _entry_to_out(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()


@router.get("/{entry_id}/history", response_model=List[schemas.EntryVersionOut])
def get_entry_history(entry_id: str, db: Session = Depends(get_db)):
    entry = db.query(models.Entry).filter(models.Entry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return [
        schemas.EntryVersionOut(
            id=v.id,
            entry_id=v.entry_id,
            title=v.title,
            content=v.content,
            tags=_str_to_tags(v.tags),
            category=v.category,
            created_at=v.created_at,
        )
        for v in entry.versions
    ]
