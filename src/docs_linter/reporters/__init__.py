"""Output reporters for lint results."""

from docs_linter.reporters.terminal import TerminalReporter
from docs_linter.reporters.json_reporter import JsonReporter

__all__ = ["TerminalReporter", "JsonReporter"]
