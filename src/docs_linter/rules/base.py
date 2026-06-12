"""Base classes for documentation style rules."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


class Severity(Enum):
    """Violation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Violation:
    """A single style violation found in a document."""
    file: str
    line: int
    column: int
    rule_id: str
    rule_name: str
    severity: Severity
    message: str
    suggestion: str
    context: str

    def __str__(self):
        return f"{self.file}:{self.line}:{self.column} [{self.severity.value}] {self.rule_id}: {self.message}"


class Rule(ABC):
    """Base class for all documentation style rules.

    Subclasses must define:
        id: Unique rule identifier (e.g., "DL001")
        name: Short human-readable name (e.g., "no-passive-voice")
        description: One-line explanation of what the rule checks

    And implement:
        check(): Examine a line of prose and return any violations
    """

    id: str
    name: str
    description: str
    severity: Severity = Severity.WARNING

    @abstractmethod
    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        """Check a single line of prose text for style violations.

        Args:
            text: The prose text to check (code blocks already stripped).
            line_num: Original line number in the source file.
            file_path: Path to the file being checked.

        Returns:
            A list of Violation objects found in this line.
        """
        ...

    def _make_violation(
        self,
        file_path: str,
        line_num: int,
        column: int,
        message: str,
        suggestion: str,
        context: str,
    ) -> Violation:
        """Helper to create a Violation with this rule's metadata."""
        return Violation(
            file=file_path,
            line=line_num,
            column=column,
            rule_id=self.id,
            rule_name=self.name,
            severity=self.severity,
            message=message,
            suggestion=suggestion,
            context=context,
        )
