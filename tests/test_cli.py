"""Tests for the CLI interface."""

import pytest
from click.testing import CliRunner

from docs_linter.cli import main


@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_list_rules(runner):
    result = runner.invoke(main, ["--list-rules"])
    assert result.exit_code == 0
    assert "DL001" in result.output
    assert "DL005" in result.output
    assert "no-passive-voice" in result.output


def test_no_paths_errors(runner):
    result = runner.invoke(main, [])
    assert result.exit_code == 1
    assert "No paths specified" in result.output


def test_init_creates_config(runner, tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ["--init"])
        assert result.exit_code == 0
        assert "Created .docs-linter.yml" in result.output


def test_lint_good_file(runner, tmp_path):
    good_file = tmp_path / "good.md"
    good_file.write_text("# Set up authentication\n\nRun the setup command.\n")

    result = runner.invoke(main, [str(good_file)])
    assert result.exit_code == 0
    assert "No issues found" in result.output


def test_lint_bad_file(runner, tmp_path):
    bad_file = tmp_path / "bad.md"
    bad_file.write_text("The system will will restart soon.\n")

    result = runner.invoke(main, [str(bad_file)])
    assert result.exit_code == 1


def test_json_output(runner, tmp_path):
    bad_file = tmp_path / "test.md"
    bad_file.write_text("Click the the button.\n")

    result = runner.invoke(main, [str(bad_file), "--format", "json"])
    assert '"rule_id"' in result.output
    assert '"DL005"' in result.output


def test_rule_filter(runner, tmp_path):
    test_file = tmp_path / "test.md"
    test_file.write_text("The file is created by the system.\nThe the doubled word.\n")

    # Only check for doubled words
    result = runner.invoke(main, [str(test_file), "--rule", "DL005"])
    assert "DL005" in result.output
    # DL001 (passive) should not appear
    assert "DL001" not in result.output
