"""Command-line interface for docs-linter."""

import sys

import click

from docs_linter import __version__
from docs_linter.config import generate_default_config, load_config
from docs_linter.linter import Linter
from docs_linter.reporters.json_reporter import JsonReporter
from docs_linter.reporters.terminal import TerminalReporter
from docs_linter.rules import get_all_rules
from docs_linter.rules.base import Severity


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True))
@click.option("-c", "--config", "config_path", type=click.Path(), help="Path to config file")
@click.option(
    "-f", "--format", "output_format",
    type=click.Choice(["terminal", "json"]),
    default="terminal",
    help="Output format",
)
@click.option(
    "--severity",
    type=click.Choice(["error", "warning", "info"]),
    default=None,
    help="Minimum severity to report",
)
@click.option("--rule", "rules", multiple=True, help="Run only specific rule(s)")
@click.option("--no-color", is_flag=True, help="Disable colored output")
@click.option("-v", "--verbose", is_flag=True, help="Show context for each violation")
@click.option("--init", "do_init", is_flag=True, help="Generate a default config file")
@click.option("--list-rules", is_flag=True, help="List all available rules")
@click.version_option(version=__version__)
def main(paths, config_path, output_format, severity, rules, no_color, verbose, do_init, list_rules):
    """Lint documentation files against style rules.

    Pass one or more file paths or directories to check.

    \b
    Examples:
        docs-linter docs/
        docs-linter README.md docs/guide.md
        docs-linter . --rule DL001 --rule DL005
        docs-linter docs/ --format json
    """
    # Handle --init
    if do_init:
        config_content = generate_default_config()
        with open(".docs-linter.yml", "w") as f:
            f.write(config_content)
        click.echo("Created .docs-linter.yml with default configuration.")
        return

    # Handle --list-rules
    if list_rules:
        _print_rules()
        return

    # Require paths for linting
    if not paths:
        click.echo("Error: No paths specified. Use --help for usage.", err=True)
        sys.exit(1)

    # Load config
    config = load_config(config_path)

    # Apply rule filter
    if rules:
        if "rules" not in config:
            config["rules"] = {}
        all_rule_ids = {r.id for r in get_all_rules()}
        for rule_id in all_rule_ids:
            if rule_id not in rules:
                config["rules"][rule_id] = {"enabled": False}

    # Run linter
    linter = Linter(config=config)
    violations = linter.lint_paths(list(paths))

    # Filter by severity
    if severity:
        min_severity = Severity(severity)
        severity_order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
        min_level = severity_order[min_severity]
        violations = [v for v in violations if severity_order[v.severity] <= min_level]

    # Report
    if output_format == "json":
        reporter = JsonReporter()
        output = reporter.report(violations)
        click.echo(output)
    else:
        reporter = TerminalReporter(no_color=no_color, verbose=verbose)
        reporter.report(violations)

    # Exit code based on fail_on config
    if violations:
        fail_on = Severity(config.get("fail_on", "warning"))
        severity_order = {Severity.ERROR: 0, Severity.WARNING: 1, Severity.INFO: 2}
        fail_level = severity_order[fail_on]

        has_failing = any(
            severity_order[v.severity] <= fail_level for v in violations
        )
        if has_failing:
            sys.exit(1)


def _print_rules():
    """Print a table of all available rules."""
    click.echo("\nAvailable rules:\n")
    click.echo(f"  {'ID':<8} {'Name':<25} {'Severity':<10} Description")
    click.echo(f"  {'─' * 8} {'─' * 25} {'─' * 10} {'─' * 40}")

    for rule in get_all_rules():
        click.echo(
            f"  {rule.id:<8} {rule.name:<25} {rule.severity.value:<10} {rule.description}"
        )
    click.echo()


if __name__ == "__main__":
    main()
