"""
Agent Service
-------------
Builds and runs a LangGraph ReAct agent powered by DeepSeek (via OpenRouter).

Tools available to the agent:
  - get_zodiac_sign_from_birthdate → determine zodiac sign from a birthdate
  - get_sign_profile               → element, ruling planet, traits, lucky color/number
  - get_horoscope                  → real daily/weekly/monthly horoscope reading
  - get_compatibility              → compatibility summary between two signs

The agent decides which tool(s) to call based on the user's question,
then synthesises a final natural-language answer.

Uses langgraph.prebuilt.create_react_agent (modern LangGraph approach,
replaces the deprecated langchain AgentExecutor). Structure mirrors the
weather agent's agent_service.py.
"""

import json
import asyncio
import concurrent.futures

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from core.config import get_settings
from services.astrology_service import (
    zodiac_sign_from_birthdate,
    get_sign_profile,
    get_compatibility,
    get_horoscope,
)

settings = get_settings()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _run_async_in_thread(coro):
    """
    Run an async coroutine from a sync context.
    LangGraph tool calls happen inside an already-running event loop (FastAPI),
    so we spin up a fresh loop in a thread pool to avoid 'loop already running'.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(asyncio.run, coro)
        return future.result()


# ─── Tool Definitions (LangChain @tool decorator) ────────────────────────────

@tool
def tool_get_zodiac_sign_from_birthdate(birthdate: str) -> str:
    """
    Determine a person's zodiac sign from their birthdate.

    Args:
        birthdate: Date in YYYY-MM-DD format (e.g. '1994-06-12')

    Returns:
        JSON string with the sign's name, symbol, element, ruling planet,
        traits, lucky color/number, and compatible signs.
    """
    try:
        result = zodiac_sign_from_birthdate(birthdate.strip())
        return json.dumps(result, indent=2)
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Failed to determine zodiac sign for '{birthdate}': {e}"


@tool
def tool_get_sign_profile(sign: str) -> str:
    """
    Look up a zodiac sign's static profile: element, ruling planet,
    personality traits, lucky color/number, and best-match signs.

    Args:
        sign: Zodiac sign name (e.g. 'Leo', 'scorpio')

    Returns:
        JSON string with the sign's full profile.
    """
    try:
        result = get_sign_profile(sign.strip())
        return json.dumps(result, indent=2)
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Failed to look up sign '{sign}': {e}"


@tool
def tool_get_horoscope(sign: str, period: str = "daily") -> str:
    """
    Fetch a real horoscope reading for a zodiac sign.

    Args:
        sign: Zodiac sign name (e.g. 'Aries', 'pisces')
        period: One of 'daily', 'weekly', or 'monthly' (default 'daily')

    Returns:
        JSON string with the sign, period, date, and horoscope text.
    """
    try:
        result = _run_async_in_thread(get_horoscope(sign.strip(), period.strip()))
        return json.dumps(result, indent=2)
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Failed to fetch {period} horoscope for '{sign}': {e}"


@tool
def tool_get_compatibility(sign1: str, sign2: str) -> str:
    """
    Get a compatibility summary between two zodiac signs.

    Args:
        sign1: First zodiac sign name (e.g. 'Leo')
        sign2: Second zodiac sign name (e.g. 'Aquarius')

    Returns:
        JSON string indicating whether the pair is a top match, whether
        they share an element, and each sign's best-match list.
    """
    try:
        result = get_compatibility(sign1.strip(), sign2.strip())
        return json.dumps(result, indent=2)
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Failed to compare '{sign1}' and '{sign2}': {e}"


TOOLS = [
    tool_get_zodiac_sign_from_birthdate,
    tool_get_sign_profile,
    tool_get_horoscope,
    tool_get_compatibility,
]


# ─── LLM Factory ─────────────────────────────────────────────────────────────

def _build_llm() -> ChatOpenAI:
    """Instantiate the DeepSeek model via OpenRouter's OpenAI-compatible endpoint."""
    return ChatOpenAI(
        model=settings.primary_model,
        openai_api_key=settings.openrouter_api_key,
        openai_api_base=settings.openrouter_base_url,
        temperature=0.4,
        max_tokens=1024,
        default_headers={
            "HTTP-Referer": "https://astrology-agent.local",
            "X-Title": "Astrology ReAct Agent",
        },
    )


# ─── Public Interface ─────────────────────────────────────────────────────────

async def run_agent(question: str) -> dict:
    """
    Run the ReAct agent against the user's question.

    Returns:
        {
            "answer":     str,
            "tools_used": list[str],
        }
    """
    if not settings.openrouter_api_key:
        return {
            "answer": (
                "\u26a0\ufe0f OpenRouter API key is not configured. "
                "Please set OPENROUTER_API_KEY in your .env file."
            ),
            "tools_used": [],
        }

    llm = _build_llm()
    graph = create_react_agent(model=llm, tools=TOOLS)

    messages = [{"role": "user", "content": question}]
    result = await graph.ainvoke({"messages": messages})

    # ── Extract final answer ──────────────────────────────────────────────────
    final_message = result["messages"][-1]
    answer = (
        final_message.content
        if hasattr(final_message, "content")
        else str(final_message)
    )

    # ── Extract which tools were called ───────────────────────────────────────
    tools_used = []
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)
                if name and name not in tools_used:
                    tools_used.append(name)

    return {
        "answer": answer,
        "tools_used": tools_used,
    }
