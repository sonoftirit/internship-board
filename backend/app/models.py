from datetime import datetime

from pydantic import BaseModel, field_validator


class Listing(BaseModel):
    """A job listing that passed validation. Anything that doesn't fit this shape is rejected."""

    id: str
    source: str
    company_name: str
    title: str
    category: str | None = None
    locations: list[str] = []
    url: str
    sponsorship: str | None = None
    degrees: list[str] = []
    terms: list[str] = []
    active: bool = True
    is_visible: bool = True
    date_posted: datetime  # the source sends unix seconds; Pydantic converts them
    date_updated: datetime | None = None

    @field_validator("company_name", "title")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()

    @field_validator("url")
    @classmethod
    def must_be_web_link(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("must start with http:// or https://")
        return value
