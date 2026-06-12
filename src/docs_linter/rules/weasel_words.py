"""DL003: Detect weasel words and hedging language."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

WEASEL_WORDS = {
    "might": "can",
    "may": "can",
    "should": "must (if required) or can (if optional)",
    "could": "can",
    "would": "use present tense",
    "perhaps": "remove or be specific",
    "basically": "remove",
    "simply": "remove",
    "just": "remove",
    "obviously": "remove",
    "clearly": "remove",
    "easy": "remove (what's easy for you isn't easy for everyone)",
    "easily": "remove",
    "quite": "remove or quantify",
    "fairly": "remove or quantify",
    "rather": "remove or be specific",
    "somewhat": "remove or quantify",
    "probably": "remove or be specific",
}

# Build pattern that matches whole words only
_WORDS = "|".join(re.escape(w) for w in WEASEL_WORDS.keys())
WEASEL_PATTERN = re.compile(rf"\b({_WORDS})\b", re.IGNORECASE)


class WeaselWordsRule(Rule):
    """Detect hedging and weasel words that weaken technical documentation."""

    id = "DL003"
    name = "no-weasel-words"
    description = "Avoid hedging language (might, should, simply, etc.). Be direct and specific."
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for match in WEASEL_PATTERN.finditer(text):
            word = match.group(1).lower()
            col = match.start() + 1
            replacement = WEASEL_WORDS[word]

            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=col,
                message=f'Weasel word: "{match.group(1)}"',
                suggestion=f"Replace with: {replacement}",
                context=text.rstrip(),
            ))

        return violations
