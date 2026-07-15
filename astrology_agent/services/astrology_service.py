"""
Astrology Service
------------------
Thin async HTTP client wrapping one free, no-key-needed API:
  - freehoroscopeapi.com  →  daily/weekly/monthly horoscope text per sign

Plus local (no external call) zodiac lookups and compatibility scoring,
backed by services/zodiac_data.py.

Used exclusively by the LangGraph tools in agent_service.py — mirrors
the role weather_service.py plays for the weather agent.
"""

import httpx

from core.config import get_settings
from services.zodiac_data import (
    ZODIAC_SIGNS,
    get_sign,
    sign_from_isodate,
)

settings = get_settings()

_VALID_PERIODS = {"daily", "weekly", "monthly"}


def zodiac_sign_from_birthdate(birthdate: str) -> dict:
    """
    Convert an ISO date string (YYYY-MM-DD) to its zodiac sign profile.
    Raises ValueError if the date string is malformed.
    """
    try:
        sign = sign_from_isodate(birthdate)
    except ValueError:
        raise ValueError(f"'{birthdate}' is not a valid date. Use YYYY-MM-DD format.")
    return sign


def get_sign_profile(sign_name: str) -> dict:
    """
    Look up a sign's static profile (element, ruling planet, traits,
    lucky color/number, compatible signs) by name or key.
    Raises ValueError if the sign isn't recognized.
    """
    sign = get_sign(sign_name)
    if not sign:
        valid = ", ".join(s["name"] for s in ZODIAC_SIGNS)
        raise ValueError(f"'{sign_name}' is not a recognized zodiac sign. Valid signs: {valid}")
    return sign


def get_compatibility(sign1_name: str, sign2_name: str) -> dict:
    """
    Returns a compatibility summary between two signs, based on each
    sign's static list of best-match signs.
    """
    sign1 = get_sign_profile(sign1_name)
    sign2 = get_sign_profile(sign2_name)

    is_match = sign2["name"] in sign1["compatible"] or sign1["name"] in sign2["compatible"]
    same_element = sign1["element"] == sign2["element"]

    return {
        "sign1": sign1["name"],
        "sign2": sign2["name"],
        "is_top_match": is_match,
        "same_element": same_element,
        "sign1_element": sign1["element"],
        "sign2_element": sign2["element"],
        "sign1_best_matches": sign1["compatible"],
        "sign2_best_matches": sign2["compatible"],
    }


async def get_horoscope(sign_name: str, period: str = "daily") -> dict:
    """
    Fetch a real horoscope reading from freehoroscopeapi.com for the
    given sign and period ('daily', 'weekly', or 'monthly').
    Raises ValueError for an unrecognized sign or period.
    """
    sign = get_sign_profile(sign_name)  # validates + normalizes the name

    period = period.strip().lower()
    if period not in _VALID_PERIODS:
        raise ValueError(f"period must be one of: {', '.join(sorted(_VALID_PERIODS))}")

    url = f"{settings.horoscope_api_base_url}/get-horoscope/{period}"
    params = {"sign": sign["key"]}

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    payload = data.get("data", {})
    return {
        "sign": sign["name"],
        "period": payload.get("period", period),
        "date": payload.get("date"),
        "horoscope": payload.get("horoscope", ""),
    }
