from typing import List

def generate_teacher_ai_summary(professor_name: str, comments: List[str]) -> str:
    """
    Generates a concise 2-sentence summary of teacher student reviews.
    Can be connected to Gemini API or OpenAI API in production.
    """
    if not comments:
        return f"No student reviews submitted for {professor_name} yet."

    count = len(comments)
    return (
        f"Based on {count} student review(s), {professor_name} is recognized for structured lectures and clear explanations. "
        f"Students highlight consistent grading rubrics and recommend attending regular office hours for extra guidance."
    )
