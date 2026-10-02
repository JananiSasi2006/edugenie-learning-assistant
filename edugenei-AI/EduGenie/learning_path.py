from ai_client import generate_text, demo_message

async def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = (
        f"Create a personalized learning path for: {topic}\nLearner level: {level}\n\n"
        "Organize it from beginner to advanced. Include a sensible timeline, weekly topics, "
        "hands-on exercises, a small final project, and suggestions for learning resources. "
        "Do not invent specific URLs; name reliable resource types or well-known documentation sites."
    )
    result = await generate_text(prompt)
    if result:
        return result
    return (
        f"Learning path: {topic}\n\n"
        "Week 1 — Foundations: learn key terms and basic concepts; write short notes.\n"
        "Week 2 — Core skills: work through guided examples and beginner exercises.\n"
        "Week 3 — Intermediate practice: solve small problems and review mistakes.\n"
        "Week 4 — Build: create a mini project using the concepts learned.\n"
        "Week 5 — Advanced topics: explore optimization, common patterns, and best practices.\n"
        "Week 6 — Final project and revision: build something independently and explain your choices.\n\n"
        "Resources: official documentation, beginner tutorials, and practice exercises."
    ) if topic.strip() else demo_message("Learning recommendations", topic)
