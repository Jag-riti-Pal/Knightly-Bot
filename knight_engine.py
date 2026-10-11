import json
import re
from pathlib import Path

GRAMMAR_RULES = [
    (r"\byou're\b", "thou art"),
    (r"\byou\s+are\b", "thou art"),
    (r"\byou've\b", "thou hast"),
    (r"\byou\s+have\b", "thou hast"),
    (r"\byour\b", "thy"),
    (r"\byours\b", "thine"),
    (r"\byou\b", "thou"),
    (r"\bdo\s+not\b", "dost not"),
    (r"\bdon't\b", "dost not"),
    (r"\bdoes\s+not\b", "doth not"),
    (r"\bdoesn't\b", "doth not"),
    (r"\bare\b", "art"),
]


class ChivalryTranslator:
    def __init__(self, dict_path: str = "data/dictionary.json"):
        with open(dict_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.phrases = data.get("phrases", {})
        self.vocab = data.get("vocab", {})

    def transform(self, text: str) -> str:
        output = text

        # 1. Multi-word phrases first
        for phrase, replacement in self.phrases.items():
            pattern = rf"\b{re.escape(phrase)}\b"
            output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)

        # 2. Vocabulary words
        for word, replacement in self.vocab.items():
            pattern = rf"\b{re.escape(word)}\b"
            output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)

        # 3. Old English pronouns and verbs
        for pattern, replacement in GRAMMAR_RULES:
            output = re.sub(pattern, replacement, output, flags=re.IGNORECASE)

        # 4. Clean sentence capitalization
        sentences = re.split(r"([.!?]\s*)", output)
        return "".join(s.capitalize() if s and s[0].isalpha() else s for s in sentences)