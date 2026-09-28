"""ORM models for the knowledge store."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


def _new_uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class EntryVersion(Base):
    __tablename__ = "entry_versions"

    id = Column(String, primary_key=True, default=_new_uuid)
    entry_id = Column(String, ForeignKey("entries.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=False, default="")  # comma-separated
    category = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=_now)

    entry = relationship("Entry", back_populates="versions")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(String, primary_key=True, default=_new_uuid)
    created_at = Column(DateTime, nullable=False, default=_now)
    updated_at = Column(DateTime, nullable=False, default=_now, onupdate=_now)

    # Current content (denormalised for fast lookup)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=False, default="")  # comma-separated
    category = Column(String, nullable=True)

    versions = relationship(
        "EntryVersion",
        back_populates="entry",
        cascade="all, delete-orphan",
        order_by="EntryVersion.created_at",
    )
