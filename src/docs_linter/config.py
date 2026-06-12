"""Configuration loading and management."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

DEFAULT_CONFIG_NAME = ".docs-linter.yml"

DEFAULT_CONFIG = {
    "file_types": ["*.md"],
    "exclude": [
        "node_modules/**",
        "vendor/**",
        ".git/**",
        ".venv/**",
        "venv/**",
    ],
    "rules": {},
    "fail_on": "warning",
}


def find_config(start_path: Optional[str] = None) -> Optional[Path]:
    """Search for a config file starting from the given path, moving up."""
    if start_path:
        path = Path(start_path)
    else:
        path = Path.cwd()

    # Check explicit path
    if path.is_file() and path.name == DEFAULT_CONFIG_NAME:
        return path

    # Search up directory tree
    current = path if path.is_dir() else path.parent
    while current != current.parent:
        config_path = current / DEFAULT_CONFIG_NAME
        if config_path.exists():
            return config_path
        current = current.parent

    # Check root
    config_path = current / DEFAULT_CONFIG_NAME
    if config_path.exists():
        return config_path

    return None


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from a YAML file, merging with defaults.

    Args:
        config_path: Explicit path to config file. If None, searches up from cwd.

    Returns:
        Merged configuration dictionary.
    """
    config = DEFAULT_CONFIG.copy()

    # Find config file
    if config_path:
        path = Path(config_path)
        if not path.exists():
            return config
    else:
        path = find_config()
        if path is None:
            return config

    # Load and merge
    with open(path, "r") as f:
        user_config = yaml.safe_load(f) or {}

    # Merge top-level keys
    for key in ("file_types", "exclude", "fail_on"):
        if key in user_config:
            config[key] = user_config[key]

    # Merge rules (per-rule overrides)
    if "rules" in user_config:
        config["rules"] = user_config["rules"]

    return config


def get_rule_config(config: Dict[str, Any], rule_id: str) -> Dict[str, Any]:
    """Get configuration for a specific rule.

    Returns:
        Dict with 'enabled', 'severity', and 'options' keys.
    """
    defaults = {"enabled": True, "severity": None, "options": {}}
    rule_overrides = config.get("rules", {}).get(rule_id, {})

    if isinstance(rule_overrides, dict):
        defaults.update(rule_overrides)

    return defaults


def generate_default_config() -> str:
    """Generate a commented default config file."""
    return """# .docs-linter.yml
# Configuration for docs-linter
# See: https://github.com/henrytamm/docs-linter

# File types to lint
file_types:
  - "*.md"

# Glob patterns to exclude
exclude:
  - "node_modules/**"
  - "vendor/**"
  - ".git/**"
  - ".venv/**"

# Rule configuration
# Override severity or disable rules here.
# Available rules: DL001-DL012
rules:
  DL001:  # no-passive-voice
    enabled: true
    severity: warning
  DL002:  # no-future-tense
    enabled: true
    severity: warning
  DL003:  # no-weasel-words
    enabled: true
    severity: warning
  DL004:  # no-permissive-language
    enabled: true
    severity: warning
  DL005:  # no-doubled-words
    enabled: true
    severity: error
  DL007:  # sentence-length
    enabled: true
    severity: info
    options:
      max_words: 30
  DL008:  # heading-style
    enabled: true
    severity: warning
  DL010:  # no-placeholder-text
    enabled: true
    severity: error
  DL011:  # no-first-person
    enabled: true
    severity: warning
  DL012:  # no-click-here
    enabled: true
    severity: warning

# Minimum severity to exit non-zero (for CI)
# Options: error, warning, info
fail_on: warning
"""
