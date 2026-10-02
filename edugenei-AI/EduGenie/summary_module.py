from ai_client import generate_text, demo_message

async def summarize_text(text: str, level: str = "Beginner") -> str:
    prompt = (
        f"Summarize the following educational text for a {level.lower()} learner. "
        "Keep the main facts, remove repetition, and finish with 3 key takeaways. "
        "Do not add facts that are not supported by the text.\n\n"
        f"TEXT:\n{text}"
    )
    result = await generate_text(prompt)
    if result:
        return result
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    if sentences:
        return ". ".join(sentences[:3]) + ("." if len(sentences) else "")
    return demo_message("Summarization", text)
