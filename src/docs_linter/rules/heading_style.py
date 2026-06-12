"""DL008: Check heading style conventions."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Match Markdown headings
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")


class HeadingStyleRule(Rule):
    """Ensure headings follow style conventions (no trailing punctuation, sentence case)."""

    id = "DL008"
    name = "heading-style"
    description = "Headings: no trailing punctuation, use sentence case for task topics."
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        match = HEADING_PATTERN.match(text.strip())
        if not match:
            return violations

        heading_text = match.group(2).strip()

        # Check for trailing punctuation (except ? which is sometimes OK)
        if heading_text and heading_text[-1] in ".!;:,":
            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=len(match.group(1)) + 2 + len(heading_text),
                message=f'Heading has trailing punctuation: "{heading_text[-1]}"',
                suggestion="Remove trailing punctuation from headings.",
                context=text.rstrip(),
            ))

        # Check if heading is phrased as a question (info only)
        if heading_text.endswith("?"):
            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=1,
                message="Heading phrased as a question",
                suggestion="Rephrase as a statement or imperative (e.g., 'Configure X' instead of 'How do I configure X?').",
                context=text.rstrip(),
            ))

        return violations
