"""JSON output reporter for CI integration."""

import json
from typing import List

from docs_linter.rules.base import Violation


class JsonReporter:
    """Output lint results as JSON for CI/CD pipelines."""

    def report(self, violations: List[Violation]) -> str:
        """Return violations as a JSON string."""
        output = {
            "total": len(violations),
            "errors": sum(1 for v in violations if v.severity.value == "error"),
            "warnings": sum(1 for v in violations if v.severity.value == "warning"),
            "info": sum(1 for v in violations if v.severity.value == "info"),
            "violations": [
                {
                    "file": v.file,
                    "line": v.line,
                    "column": v.column,
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity.value,
                    "message": v.message,
                    "suggestion": v.suggestion,
                }
                for v in violations
            ],
        }

        return json.dumps(output, indent=2)
