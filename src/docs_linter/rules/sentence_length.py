"""DL007: Detect overly long sentences."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Simple sentence boundary: period/exclamation/question + space + capital letter
# or end of line after period
SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')

DEFAULT_MAX_WORDS = 30


class SentenceLengthRule(Rule):
    """Flag sentences that exceed a configurable word count."""

    id = "DL007"
    name = "sentence-length"
    description = "Keep sentences short and scannable. Split long sentences."
    severity = Severity.INFO

    def __init__(self, max_words: int = DEFAULT_MAX_WORDS):
        self.max_words = max_words

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        # Skip headings, list items (they get a pass on length)
        stripped = text.strip()
        if stripped.startswith(("#", "-", "*", "1.", ">")):
            return violations

        # Split into sentences
        sentences = SENTENCE_SPLIT.split(text)

        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)

            if word_count > self.max_words:
                col = text.find(sentence) + 1 if sentence in text else 1

                violations.append(self._make_violation(
                    file_path=file_path,
                    line_num=line_num,
                    column=col,
                    message=f"Sentence has {word_count} words (max: {self.max_words})",
                    suggestion="Split into shorter sentences for readability.",
                    context=text.rstrip(),
                ))

        return violations
