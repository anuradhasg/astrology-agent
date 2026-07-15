"""
Zodiac Reference Data
----------------------
Static, no external calls: date ranges, symbols, elements, ruling planets,
traits, lucky color/number, and compatibility for all 12 signs.
Date-boundary logic verified against all 12 sign transitions including
the Capricorn year-wrap (Dec 22 -> Jan 19).
"""

from datetime import date

ZODIAC_SIGNS = [
    {
        "key": "aries", "name": "Aries", "symbol": "\u2648",
        "start": (3, 21), "end": (4, 19),
        "element": "Fire", "ruling_planet": "Mars",
        "traits": ["Bold", "Energetic", "Competitive", "Direct"],
        "compatible": ["Leo", "Sagittarius", "Gemini"],
        "lucky_color": "Red", "lucky_number": 9,
    },
    {
        "key": "taurus", "name": "Taurus", "symbol": "\u2649",
        "start": (4, 20), "end": (5, 20),
        "element": "Earth", "ruling_planet": "Venus",
        "traits": ["Steady", "Patient", "Sensual", "Determined"],
        "compatible": ["Virgo", "Capricorn", "Cancer"],
        "lucky_color": "Emerald Green", "lucky_number": 6,
    },
    {
        "key": "gemini", "name": "Gemini", "symbol": "\u264A",
        "start": (5, 21), "end": (6, 20),
        "element": "Air", "ruling_planet": "Mercury",
        "traits": ["Curious", "Witty", "Adaptable", "Expressive"],
        "compatible": ["Libra", "Aquarius", "Aries"],
        "lucky_color": "Yellow", "lucky_number": 5,
    },
    {
        "key": "cancer", "name": "Cancer", "symbol": "\u264B",
        "start": (6, 21), "end": (7, 22),
        "element": "Water", "ruling_planet": "Moon",
        "traits": ["Nurturing", "Intuitive", "Loyal", "Emotional"],
        "compatible": ["Scorpio", "Pisces", "Taurus"],
        "lucky_color": "Silver", "lucky_number": 2,
    },
    {
        "key": "leo", "name": "Leo", "symbol": "\u264C",
        "start": (7, 23), "end": (8, 22),
        "element": "Fire", "ruling_planet": "Sun",
        "traits": ["Confident", "Generous", "Charismatic", "Dramatic"],
        "compatible": ["Aries", "Sagittarius", "Libra"],
        "lucky_color": "Gold", "lucky_number": 1,
    },
    {
        "key": "virgo", "name": "Virgo", "symbol": "\u264D",
        "start": (8, 23), "end": (9, 22),
        "element": "Earth", "ruling_planet": "Mercury",
        "traits": ["Analytical", "Meticulous", "Practical", "Modest"],
        "compatible": ["Taurus", "Capricorn", "Scorpio"],
        "lucky_color": "Navy Blue", "lucky_number": 5,
    },
    {
        "key": "libra", "name": "Libra", "symbol": "\u264E",
        "start": (9, 23), "end": (10, 22),
        "element": "Air", "ruling_planet": "Venus",
        "traits": ["Diplomatic", "Charming", "Fair-minded", "Social"],
        "compatible": ["Gemini", "Aquarius", "Leo"],
        "lucky_color": "Rose Pink", "lucky_number": 6,
    },
    {
        "key": "scorpio", "name": "Scorpio", "symbol": "\u264F",
        "start": (10, 23), "end": (11, 21),
        "element": "Water", "ruling_planet": "Pluto",
        "traits": ["Intense", "Magnetic", "Resourceful", "Private"],
        "compatible": ["Cancer", "Pisces", "Virgo"],
        "lucky_color": "Deep Crimson", "lucky_number": 8,
    },
    {
        "key": "sagittarius", "name": "Sagittarius", "symbol": "\u2650",
        "start": (11, 22), "end": (12, 21),
        "element": "Fire", "ruling_planet": "Jupiter",
        "traits": ["Adventurous", "Optimistic", "Philosophical", "Blunt"],
        "compatible": ["Aries", "Leo", "Aquarius"],
        "lucky_color": "Purple", "lucky_number": 3,
    },
    {
        "key": "capricorn", "name": "Capricorn", "symbol": "\u2651",
        "start": (12, 22), "end": (1, 19),
        "element": "Earth", "ruling_planet": "Saturn",
        "traits": ["Disciplined", "Ambitious", "Reserved", "Responsible"],
        "compatible": ["Taurus", "Virgo", "Pisces"],
        "lucky_color": "Charcoal Grey", "lucky_number": 4,
    },
    {
        "key": "aquarius", "name": "Aquarius", "symbol": "\u2652",
        "start": (1, 20), "end": (2, 18),
        "element": "Air", "ruling_planet": "Uranus",
        "traits": ["Independent", "Inventive", "Idealistic", "Unconventional"],
        "compatible": ["Gemini", "Libra", "Sagittarius"],
        "lucky_color": "Electric Blue", "lucky_number": 7,
    },
    {
        "key": "pisces", "name": "Pisces", "symbol": "\u2653",
        "start": (2, 19), "end": (3, 20),
        "element": "Water", "ruling_planet": "Neptune",
        "traits": ["Dreamy", "Compassionate", "Artistic", "Sensitive"],
        "compatible": ["Cancer", "Scorpio", "Capricorn"],
        "lucky_color": "Sea Green", "lucky_number": 3,
    },
]

_BY_KEY = {s["key"]: s for s in ZODIAC_SIGNS}
_BY_NAME = {s["name"].lower(): s for s in ZODIAC_SIGNS}


def get_sign_by_key(key: str) -> dict | None:
    return _BY_KEY.get(key.strip().lower()) if key else None


def get_sign_by_name(name: str) -> dict | None:
    return _BY_NAME.get(name.strip().lower()) if name else None


def get_sign(identifier: str) -> dict | None:
    """Looks up a sign by either its key ('aries') or display name ('Aries')."""
    return get_sign_by_key(identifier) or get_sign_by_name(identifier)


def sign_from_date(month: int, day: int) -> dict:
    """Returns the zodiac sign dict for a given month/day, handling the
    one sign (Capricorn) whose range wraps across the new year."""
    for sign in ZODIAC_SIGNS:
        start_m, start_d = sign["start"]
        end_m, end_d = sign["end"]
        if start_m <= end_m:
            in_range = (month == start_m and day >= start_d) or \
                       (month == end_m and day <= end_d) or \
                       (start_m < month < end_m)
        else:
            in_range = (month == start_m and day >= start_d) or \
                       (month == end_m and day <= end_d)
        if in_range:
            return sign
    return ZODIAC_SIGNS[0]  # unreachable given full year coverage


def sign_from_isodate(iso_date: str) -> dict:
    d = date.fromisoformat(iso_date)
    return sign_from_date(d.month, d.day)
