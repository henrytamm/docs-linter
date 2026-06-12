"""Core linter engine: file discovery, parsing, rule application."""

import fnmatch
from pathlib import Path
from typing import Dict, List, Any, Optional

from docs_linter.config import get_rule_config, load_config
from docs_linter.parsers.markdown import MarkdownParser
from docs_linter.rules import get_all_rules
from docs_linter.rules.base import Rule, Severity, Violation


class Linter:
    """Orchestrates file discovery, parsing, and rule checking.

    Usage:
        linter = Linter(config=load_config())
        violations = linter.lint_paths(["docs/", "README.md"])
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or load_config()
        self.parser = MarkdownParser()
        self.rules = self._init_rules()

    def _init_rules(self) -> List[Rule]:
        """Initialize rules based on configuration."""
        active_rules = []

        for rule in get_all_rules():
            rule_config = get_rule_config(self.config, rule.id)

            # Skip disabled rules
            if not rule_config.get("enabled", True):
                continue

            # Override severity if configured
            severity_override = rule_config.get("severity")
            if severity_override:
                try:
                    rule.severity = Severity(severity_override)
                except ValueError:
                    pass

            active_rules.append(rule)

        return active_rules

    def lint_paths(self, paths: List[str]) -> List[Violation]:
        """Lint all matching files under the given paths.

        Args:
            paths: List of file paths or directories to lint.

        Returns:
            All violations found across all files.
        """
        violations = []
        files = self._discover_files(paths)

        for file_path in files:
            file_violations = self.lint_file(file_path)
            violations.extend(file_violations)

        return violations

    def lint_file(self, file_path: str) -> List[Violation]:
        """Lint a single file.

        Args:
            file_path: Path to the file to lint.

        Returns:
            Violations found in this file.
        """
        path = Path(file_path)

        if not path.exists():
            return []

        content = path.read_text(encoding="utf-8", errors="replace")
        prose_lines = self.parser.parse(content)

        violations = []
        for prose_line in prose_lines:
            for rule in self.rules:
                rule_violations = rule.check(
                    prose_line.text,
                    prose_line.line_num,
                    str(file_path),
                )
                violations.extend(rule_violations)

        return violations

    def _discover_files(self, paths: List[str]) -> List[str]:
        """Find all lintable files under the given paths."""
        files = []
        file_types = self.config.get("file_types", ["*.md"])
        exclude_patterns = self.config.get("exclude", [])

        for path_str in paths:
            path = Path(path_str)

            if path.is_file():
                if self._matches_file_types(path, file_types):
                    if not self._is_excluded(path, exclude_patterns):
                        files.append(str(path))
            elif path.is_dir():
                for file_type in file_types:
                    for match in path.rglob(file_type):
                        if match.is_file() and not self._is_excluded(match, exclude_patterns):
                            files.append(str(match))

        return sorted(set(files))

    def _matches_file_types(self, path: Path, file_types: List[str]) -> bool:
        """Check if a file matches any of the configured file types."""
        for pattern in file_types:
            if fnmatch.fnmatch(path.name, pattern):
                return True
        return False

    def _is_excluded(self, path: Path, patterns: List[str]) -> bool:
        """Check if a path matches any exclusion pattern."""
        path_str = str(path)
        for pattern in patterns:
            if fnmatch.fnmatch(path_str, f"*/{pattern}") or fnmatch.fnmatch(path_str, pattern):
                return True
        return False
