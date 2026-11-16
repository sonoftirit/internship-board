import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.ingest import validate_listings
from app.models import Listing

FIXTURE = Path(__file__).parent.parent / "fixtures" / "sample_listings.json"


@pytest.fixture
def raw_listings() -> list[dict]:
    return json.loads(FIXTURE.read_text())


def test_valid_listing_converts_unix_seconds_to_utc_datetime(raw_listings):
    listing = Listing.model_validate(raw_listings[0])
    assert listing.date_posted == datetime(2026, 11, 10, 0, 0, tzinfo=timezone.utc)


def test_company_name_is_trimmed(raw_listings):
    listing = Listing.model_validate(raw_listings[1])
    assert listing.company_name == "Amazon"


def test_rejects_non_web_url():
    with pytest.raises(ValidationError):
        Listing.model_validate(
            {
                "id": "x",
                "source": "s",
                "company_name": "C",
                "title": "T",
                "date_posted": 0,
                "url": "mailto:jobs@example.com",
            }
        )


def test_rejects_blank_title():
    with pytest.raises(ValidationError):
        Listing.model_validate(
            {
                "id": "x",
                "source": "s",
                "company_name": "C",
                "title": "   ",
                "date_posted": 0,
                "url": "https://example.com",
            }
        )


def test_rejects_blank_company_name():
    with pytest.raises(ValidationError):
        Listing.model_validate(
            {
                "id": "x",
                "source": "s",
                "company_name": " ",
                "title": "SWE",
                "date_posted": 0,
                "url": "https://example.com",
            }
        )


def test_validate_listings_keeps_good_and_counts_skipped(raw_listings):
    valid, skipped = validate_listings(raw_listings)
    assert [listing.id for listing in valid] == ["good-1", "good-2"]
    assert skipped == {"hidden": 1, "invalid": 3}
