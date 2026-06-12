"""DL001: Detect passive voice in documentation."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Common past participles found in technical documentation
PAST_PARTICIPLES = [
    "accepted", "accessed", "accomplished", "achieved", "added",
    "administered", "affected", "allowed", "applied", "assigned",
    "associated", "attached", "authenticated", "authorized",
    "built", "calculated", "called", "captured", "caused",
    "changed", "checked", "chosen", "cleared", "closed",
    "collected", "combined", "completed", "composed", "compressed",
    "configured", "confirmed", "connected", "considered", "contained",
    "converted", "copied", "created", "customized",
    "defined", "deleted", "delivered", "deployed", "described",
    "designed", "detected", "determined", "developed", "disabled",
    "discovered", "displayed", "distributed", "documented", "downloaded",
    "enabled", "encrypted", "enforced", "entered", "established",
    "evaluated", "executed", "expected", "exported", "exposed",
    "extracted",
    "fetched", "filtered", "fixed", "formatted", "found",
    "generated", "given", "granted", "grouped",
    "handled", "hidden", "hosted",
    "identified", "ignored", "implemented", "imported", "improved",
    "included", "indexed", "ingested", "initialized", "inserted",
    "installed", "integrated", "interpreted", "introduced", "invoked",
    "issued",
    "kept", "known",
    "launched", "limited", "listed", "loaded", "located", "locked",
    "logged",
    "made", "maintained", "managed", "mapped", "marked", "measured",
    "merged", "migrated", "modified", "monitored", "mounted", "moved",
    "named", "needed", "notified",
    "observed", "obtained", "opened", "operated", "organized",
    "overridden", "overwritten",
    "parsed", "passed", "performed", "permitted", "placed", "populated",
    "posted", "powered", "presented", "prevented", "processed",
    "produced", "programmed", "prompted", "protected", "provided",
    "published", "pulled", "pushed",
    "queried", "queued",
    "raised", "read", "received", "recognized", "recommended",
    "recorded", "reduced", "referenced", "refreshed", "registered",
    "rejected", "released", "removed", "renamed", "rendered",
    "replaced", "reported", "represented", "required", "reset",
    "resolved", "restarted", "restored", "restricted", "retained",
    "retrieved", "returned", "revoked", "routed", "run",
    "saved", "scanned", "scheduled", "secured", "selected", "sent",
    "served", "set", "shared", "shown", "signed", "skipped",
    "sorted", "specified", "split", "started", "stopped", "stored",
    "streamed", "structured", "submitted", "supported", "suspended",
    "synced", "synchronized",
    "taken", "terminated", "tested", "thrown", "tracked", "transferred",
    "transformed", "transmitted", "triggered", "truncated", "turned",
    "updated", "upgraded", "uploaded", "used", "utilized",
    "validated", "verified", "viewed",
    "warned", "watched", "written",
]

# Regex pattern: auxiliary verb + optional adverb + past participle
_AUX_VERBS = r"(?:is|are|was|were|been|being|be|get|gets|got|gotten)"
_ADVERB = r"(?:\s+\w+ly)?"
_PARTICIPLES = "|".join(PAST_PARTICIPLES)
PASSIVE_PATTERN = re.compile(
    rf"\b({_AUX_VERBS}){_ADVERB}\s+({_PARTICIPLES})\b",
    re.IGNORECASE,
)


class PassiveVoiceRule(Rule):
    """Detect passive voice constructions in technical documentation."""

    id = "DL001"
    name = "no-passive-voice"
    description = "Avoid passive voice. Use active voice to clarify who or what performs the action."
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for match in PASSIVE_PATTERN.finditer(text):
            aux = match.group(1)
            participle = match.group(2)
            col = match.start() + 1

            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=col,
                message=f'Passive voice: "{match.group(0)}"',
                suggestion=f"Rewrite in active voice. Who performs the action?",
                context=text.rstrip(),
            ))

        return violations
