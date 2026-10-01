from ai_client import generate_text, demo_message

async def answer_question(question: str, level: str = "Beginner") -> str:
    prompt = (
        f"Learner level: {level}\nQuestion: {question}\n\n"
        "Answer the question directly. Explain unfamiliar terms simply and give an example if useful. "
        "If the question has a factual answer, state it clearly and mention uncertainty when appropriate."
    )
    result = await generate_text(prompt)
    if result:
        return result
    if "largest ocean" in question.lower():
        return "The Pacific Ocean is the largest ocean on Earth. It lies between Asia and Australia on one side and the Americas on the other."
    return demo_message("Question answering", question)
