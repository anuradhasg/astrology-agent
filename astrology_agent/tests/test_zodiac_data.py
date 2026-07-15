"""
Unit tests for services/zodiac_data.py
Run with: pytest tests/test_zodiac_data.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from services.zodiac_data import sign_from_date, sign_from_isodate, ZODIAC_SIGNS


# Every boundary date for all 12 signs, including the Capricorn year-wrap
BOUNDARY_CASES = [
    (3, 21, "Aries"), (4, 19, "Aries"),
    (4, 20, "Taurus"), (5, 20, "Taurus"),
    (5, 21, "Gemini"), (6, 20, "Gemini"),
    (6, 21, "Cancer"), (7, 22, "Cancer"),
    (7, 23, "Leo"), (8, 22, "Leo"),
    (8, 23, "Virgo"), (9, 22, "Virgo"),
    (9, 23, "Libra"), (10, 22, "Libra"),
    (10, 23, "Scorpio"), (11, 21, "Scorpio"),
    (11, 22, "Sagittarius"), (12, 21, "Sagittarius"),
    (12, 22, "Capricorn"), (12, 31, "Capricorn"),
    (1, 1, "Capricorn"), (1, 19, "Capricorn"),
    (1, 20, "Aquarius"), (2, 18, "Aquarius"),
    (2, 19, "Pisces"), (3, 20, "Pisces"),
]


@pytest.mark.parametrize("month,day,expected", BOUNDARY_CASES)
def test_sign_boundaries(month, day, expected):
    result = sign_from_date(month, day)
    assert result["name"] == expected, (
        f"{month}/{day} -> expected {expected}, got {result['name']}"
    )


def test_all_12_signs_present():
    assert len(ZODIAC_SIGNS) == 12


def test_sign_from_isodate():
    sign = sign_from_isodate("1994-06-12")
    assert sign["name"] == "Gemini"


def test_sign_from_isodate_capricorn_wrap():
    sign = sign_from_isodate("2000-12-25")
    assert sign["name"] == "Capricorn"


def test_sign_from_isodate_invalid_raises():
    with pytest.raises(ValueError):
        sign_from_isodate("not-a-date")


def test_every_day_of_year_maps_to_a_sign():
    """No gaps: every calendar day should resolve to exactly one sign."""
    import datetime
    for doy in range(1, 366):
        d = datetime.date(2023, 1, 1) + datetime.timedelta(days=doy - 1)
        sign = sign_from_date(d.month, d.day)
        assert sign is not None
        assert sign["name"] in [s["name"] for s in ZODIAC_SIGNS]
