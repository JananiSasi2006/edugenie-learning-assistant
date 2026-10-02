import os
from ai_client import generate_text, demo_message

async def explain_concept(topic: str, level: str = "Beginner") -> str:
    """Use Gemini by default; optionally use the local LaMini-Flan-T5 model."""
    provider = os.getenv("EXPLANATION_PROVIDER", "gemini").lower()
    if provider == "local":
        try:
            from transformers import pipeline
            # Lazy-load only when requested; first use downloads model weights.
            generator = _get_local_generator()
            output = generator(
                f"Explain {topic} in simple language for a {level.lower()} learner.",
                max_new_tokens=180,
                do_sample=False,
            )
            return output[0]["generated_text"].strip()
        except Exception:
            # Gracefully fall back to Gemini if local dependencies/model are unavailable.
            pass

    prompt = (
        f"Explain this concept for a {level.lower()} learner: {topic}\n"
        "Use a short definition, a simple analogy, 3 key points, and one example. "
        "Avoid unnecessary jargon."
    )
    result = await generate_text(prompt)
    return result or demo_message("Concept explanation", topic)

_LOCAL_GENERATOR = None
def _get_local_generator():
    global _LOCAL_GENERATOR
    if _LOCAL_GENERATOR is None:
        from transformers import pipeline
        model_name = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
        _LOCAL_GENERATOR = pipeline("text2text-generation", model=model_name, device=-1)
    return _LOCAL_GENERATOR
