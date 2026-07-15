from fastapi import APIRouter

from controllers.chat_controller import handle_chat
from models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Ask the AI astrology agent a question.

    The agent has access to four tools:
    - **get_zodiac_sign_from_birthdate** – determine a zodiac sign from a birthdate
    - **get_sign_profile** – element, ruling planet, traits, lucky color/number
    - **get_horoscope** – real daily/weekly/monthly horoscope reading
    - **get_compatibility** – compatibility summary between two signs

    Example questions:
    - "What's my zodiac sign if I was born on June 12, 1994?"
    - "What's today's horoscope for Leo?"
    - "Are Scorpio and Cancer compatible?"
    - "Tell me about Aquarius traits and their ruling planet."
    """
    return await handle_chat(request)
