from typing import Tuple, List

PROFANITY_WORDS = ["garbage", "idiot", "stupid", "curse", "scam", "cheat", "fraud"]

def check_profanity(text: str) -> Tuple[bool, List[str]]:
    text_lower = text.lower()
    flagged = [word for word in PROFANITY_WORDS if word in text_lower]
    return len(flagged) > 0, flagged
