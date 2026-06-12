# docs-linter

A configurable style linter for technical documentation. Checks Markdown files against prose style rules commonly enforced in technical writing teams — passive voice, future tense, weasel words, permissive language, and more.

Built for writers who want automated enforcement of the style rules they already follow manually.

## Why this exists

Style guides are great. Remembering 40+ rules while writing under deadline is not. This tool catches the mechanical violations so writers can focus on clarity, accuracy, and information architecture.

Unlike general-purpose prose linters, `docs-linter` is opinionated toward **technical documentation** — it understands that headings should be imperative, that "lets you" is a red flag, and that code blocks shouldn't be linted for grammar.

## Quick start

```bash
pip install -e .
docs-linter docs/
```

## Example output

```
docs/getting-started.md

  12:5    warning  DL001  Passive voice: "is created"
             -> Rewrite in active voice. Who performs the action?
  18:1    warning  DL002  Future tense: "will display"
             -> Use present tense instead.
  24:10   error    DL005  Doubled word: "the the"
             -> Remove the duplicate 'the'
  31:1    warning  DL004  Permissive language: "lets you"
             -> Use imperative voice instead

========================================
x 4 problems (1 error, 3 warnings)
```

## Installation

```bash
# From source
git clone https://github.com/henrytamm/docs-linter.git
cd docs-linter
pip install -e .

# With development dependencies
pip install -e ".[dev]"
```

## Usage

```bash
# Lint a directory
docs-linter docs/

# Lint specific files
docs-linter README.md docs/guide.md

# Only check specific rules
docs-linter docs/ --rule DL001 --rule DL005

# JSON output (for CI pipelines)
docs-linter docs/ --format json

# Filter by severity
docs-linter docs/ --severity error

# Show context for each violation
docs-linter docs/ --verbose

# List all available rules
docs-linter --list-rules

# Generate a config file
docs-linter --init
```

## Rules

| ID | Name | Severity | What it catches |
|----|------|----------|----------------|
| DL001 | `no-passive-voice` | warning | "is created", "was generated", "are displayed" |
| DL002 | `no-future-tense` | warning | "will restart", "shall return" |
| DL003 | `no-weasel-words` | warning | might, should, simply, basically, obviously |
| DL004 | `no-permissive-language` | warning | "lets you", "allows you to", "enables you to" |
| DL005 | `no-doubled-words` | error | "the the", "is is" |
| DL007 | `sentence-length` | info | Sentences over 30 words |
| DL008 | `heading-style` | warning | Trailing punctuation, question-style headings |
| DL010 | `no-placeholder-text` | error | TODO, FIXME, TBD, Lorem ipsum |
| DL011 | `no-first-person` | warning | "we", "our", "I" in technical docs |
| DL012 | `no-click-here` | warning | "click here", vague link text |

## Configuration

Create a `.docs-linter.yml` in your project root (or run `docs-linter --init`):

```yaml
# File types to lint
file_types:
  - "*.md"

# Glob patterns to exclude
exclude:
  - "node_modules/**"
  - ".git/**"

# Rule configuration
rules:
  DL001:
    enabled: true
    severity: warning
  DL003:
    enabled: false  # Allow weasel words in this project
  DL007:
    enabled: true
    severity: info
    options:
      max_words: 35  # Custom sentence length limit

# Exit non-zero in CI when this severity or higher is found
fail_on: warning
```

## CI integration

### GitHub Actions

```yaml
- name: Lint documentation
  run: |
    pip install docs-linter
    docs-linter docs/ --format json > lint-results.json
```

The linter exits with code 1 if any violations meet the `fail_on` threshold, making it easy to gate PRs on documentation quality.

## Design decisions

**Markdown-aware parsing** — The linter skips fenced code blocks, inline code, YAML frontmatter, and URLs. No false positives from code examples.

**Line-level checking** — Each rule operates on individual prose lines, keeping the logic simple and testable. Complex multi-line patterns (like paragraph-level analysis) are out of scope by design.

**Configurable severity** — Every rule can be set to error, warning, or info. Teams can start with warnings and ratchet up to errors as their docs improve.

**Extensible rule pattern** — Adding a new rule means creating one Python file with a `check()` method. No framework ceremony.

## Adding a custom rule

```python
# src/docs_linter/rules/my_rule.py
import re
from docs_linter.rules.base import Rule, Violation, Severity

class MyCustomRule(Rule):
    id = "DL100"
    name = "my-custom-check"
    description = "Describe what this rule catches."
    severity = Severity.WARNING

    def check(self, text, line_num, file_path):
        violations = []
        # Your detection logic here
        return violations
```

Then register it in `src/docs_linter/rules/__init__.py`.

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

## Compared to other tools

| | docs-linter | Vale | proselint |
|---|---|---|---|
| Focus | Technical docs | Configurable | General prose |
| Config | YAML | INI + packages | None |
| Rules | Built-in, opinionated | Extensive packages | Academic |
| Markdown-aware | Yes | Yes | No |
| CI-friendly | Yes (JSON, exit codes) | Yes | Limited |

`docs-linter` is intentionally smaller and more opinionated than Vale. If you want a full ecosystem with third-party style packages, use Vale. If you want a focused tool that catches the top 10 technical writing mistakes with zero setup, use this.

## License

MIT
