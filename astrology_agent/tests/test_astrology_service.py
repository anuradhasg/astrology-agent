"""
Unit tests for services/astrology_service.py (the parts that don't need
a network call — get_sign_profile, get_compatibility, birthdate lookup).
Run with: pytest tests/test_astrology_service.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from services.astrology_service import (
    zodiac_sign_from_birthdate,
    get_sign_profile,
    get_compatibility,
)


def test_zodiac_sign_from_birthdate():
    sign = zodiac_sign_from_birthdate("1994-06-12")
    assert sign["name"] == "Gemini"


def test_zodiac_sign_from_birthdate_invalid():
    with pytest.raises(ValueError):
        zodiac_sign_from_birthdate("garbage")


def test_get_sign_profile_leo():
    profile = get_sign_profile("leo")
    assert profile["element"] == "Fire"
    assert profile["ruling_planet"] == "Sun"


def test_get_sign_profile_case_insensitive():
    assert get_sign_profile("LEO")["name"] == "Leo"
    assert get_sign_profile("Leo")["name"] == "Leo"


def test_get_sign_profile_unknown_raises():
    with pytest.raises(ValueError):
        get_sign_profile("not-a-real-sign")


def test_compatibility_top_match():
    result = get_compatibility("Leo", "Sagittarius")
    assert result["is_top_match"] is True


def test_compatibility_not_a_match():
    result = get_compatibility("Leo", "Aquarius")
    assert result["is_top_match"] is False


def test_compatibility_same_element():
    result = get_compatibility("Leo", "Aries")  # both Fire signs
    assert result["same_element"] is True
