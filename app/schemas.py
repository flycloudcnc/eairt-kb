"""Pydantic schemas for request / response validation."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class EntryBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=512, description="Entry title")
    content: str = Field(..., min_length=1, description="Entry content / body")
    tags: List[str] = Field(default_factory=list, description="List of tags")
    category: Optional[str] = Field(None, max_length=128, description="Category name")


class EntryCreate(EntryBase):
    pass


class EntryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=512)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=128)


class EntryVersionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    entry_id: str
    title: str
    content: str
    tags: List[str]
    category: Optional[str]
    created_at: datetime


class EntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    content: str
    tags: List[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime


class EntryListOut(BaseModel):
    total: int
    items: List[EntryOut]


class HealthOut(BaseModel):
    status: str
