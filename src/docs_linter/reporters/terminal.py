"""Rich-powered terminal output for lint results."""

from collections import defaultdict
from typing import List

from rich.console import Console
from rich.text import Text

from docs_linter.rules.base import Severity, Violation

SEVERITY_COLORS = {
    Severity.ERROR: "red",
    Severity.WARNING: "yellow",
    Severity.INFO: "blue",
}

SEVERITY_SYMBOLS = {
    Severity.ERROR: "x",
    Severity.WARNING: "!",
    Severity.INFO: "i",
}


class TerminalReporter:
    """Format and display lint results in the terminal."""

    def __init__(self, no_color: bool = False, verbose: bool = False):
        self.console = Console(no_color=no_color)
        self.verbose = verbose

    def report(self, violations: List[Violation]) -> None:
        """Print violations grouped by file."""
        if not violations:
            self.console.print("[green]No issues found.[/green]")
            return

        # Group by file
        by_file = defaultdict(list)
        for v in violations:
            by_file[v.file].append(v)

        for file_path, file_violations in sorted(by_file.items()):
            self.console.print(f"\n[bold]{file_path}[/bold]")

            for v in sorted(file_violations, key=lambda x: (x.line, x.column)):
                color = SEVERITY_COLORS[v.severity]
                symbol = SEVERITY_SYMBOLS[v.severity]

                # Location
                loc = f"  {v.line}:{v.column}"

                # Severity tag
                sev = f"[{color}]{v.severity.value:7}[/{color}]"

                # Rule ID
                rule_id = f"[dim]{v.rule_id}[/dim]"

                # Message
                msg = v.message

                self.console.print(f"{loc:<10} {sev}  {rule_id}  {msg}")

                # Suggestion
                self.console.print(f"{'':10} [dim]   -> {v.suggestion}[/dim]")

                if self.verbose:
                    self.console.print(f"{'':10} [dim]   context: {v.context}[/dim]")

        # Summary
        self.console.print()
        self._print_summary(violations)

    def _print_summary(self, violations: List[Violation]) -> None:
        """Print a summary line with counts by severity."""
        errors = sum(1 for v in violations if v.severity == Severity.ERROR)
        warnings = sum(1 for v in violations if v.severity == Severity.WARNING)
        infos = sum(1 for v in violations if v.severity == Severity.INFO)

        total = len(violations)
        parts = []
        if errors:
            parts.append(f"[red]{errors} error{'s' if errors != 1 else ''}[/red]")
        if warnings:
            parts.append(f"[yellow]{warnings} warning{'s' if warnings != 1 else ''}[/yellow]")
        if infos:
            parts.append(f"[blue]{infos} info[/blue]")

        summary = ", ".join(parts)
        self.console.print(f"[bold]{'=' * 40}[/bold]")
        self.console.print(f"[bold]x {total} problem{'s' if total != 1 else ''}[/bold] ({summary})")
