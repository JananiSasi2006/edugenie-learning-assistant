"""Shared Google Gemini client helpers."""
import os
from functools import lru_cache
from google import genai
from google.genai import types

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

async def generate_text(prompt: str, system_instruction: str = ""):
    """Generate text with Gemini. Returns None when no key is configured."""
    client = get_client()
    if client is None:
        return None
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction or
            "You are EduGenie, a friendly educational assistant. Be accurate, clear, age-appropriate, and concise.",
            temperature=0.4,
        ),
    )
    return (response.text or "").strip()

def demo_message(feature: str, text: str) -> str:
    return (
        f"{feature} is in demo mode because GEMINI_API_KEY is not configured. "
        "Add your Google AI Studio API key to the .env file, restart the server, "
        f"and try again.\n\nYour input: {text[:500]}"
    )
