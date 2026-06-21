"""Parser + structural validator for the Upper Bound (refund_policy.md).

The handbook is the citable normative ceiling (spec §2). This module turns its
strict, token-parsable Markdown into structured objects so the orchestrator can:
  - dispatch one policy's block into spec.txt at delegation time (§1),
  - assert at Gate A that the file stays policy-centric (no code/schema/prompt),
  - assert at Gate C that the exerciser's matrix covers every CLAUSE_X (§3).

There is exactly one parser (this file); the handbook is authored to it, so a
malformed ceiling is a hard, early failure rather than a silently misread rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

START = "# REFUND_POLICY_SPEC_START"
END = "# REFUND_POLICY_SPEC_END"
VALID_STATUS = {"BINDING", "DRAFT", "DEPRECATED"}
VALID_ACTIONS = {"REIMBURSE", "DENY", "ESCALATE"}

DEFAULT_PATH = Path(__file__).resolve().parent / "refund_policy.md"


class HandbookError(ValueError):
    """Raised when the handbook violates its schema (spec §2)."""


@dataclass(frozen=True)
class NegativeVector:
    target_exploit: str
    expected_action: str        # the failsafe verdict, in VALID_ACTIONS


@dataclass(frozen=True)
class Policy:
    policy_id: str
    threat_category: str
    incident_anchor: str
    status: str
    core_property: str
    clauses: dict[str, str]            # {"CLAUSE_1": text, ...}, insertion-ordered
    negative_vector: NegativeVector
    not_claims: dict[str, str]         # {"NOT_CLAIM_1": text, ...}
    raw_block: str                     # verbatim markdown for this policy (for dispatch)

    @property
    def clause_ids(self) -> list[str]:
        return list(self.clauses)


_FIELD = {
    "threat_category": re.compile(r"\*\*Threat Category:\*\*\s*(.+)"),
    "incident_anchor": re.compile(r"\*\*Flagship Incident Anchor:\*\*\s*(.+)"),
    "status": re.compile(r"\*\*Status:\*\*\s*(\S+)"),
}
_POLICY_HEAD = re.compile(r"^##\s*POLICY_ID:\s*(\S+)\s*$", re.MULTILINE)
_CLAUSE = re.compile(r"\*\*(CLAUSE_\d+):\*\*\s*(.+)")
_NOT_CLAIM = re.compile(r"\*\*(NOT_CLAIM_\d+):\*\*\s*(.+)")
_CORE_PROP = re.compile(
    r"###\s*1\.\s*Plain English Core Property\s*\n(.*?)(?=\n###\s|\Z)", re.DOTALL)
_TARGET_EXPLOIT = re.compile(r"\*\*Target Exploit:\*\*\s*(.+)")
_EXPECTED_FAIL = re.compile(r"\*\*Expected System Failure Point:\*\*\s*(.+)")


def _action_in(text: str) -> str | None:
    """Return the single VALID_ACTION token the expected-failure line commits to."""
    hits = [a for a in VALID_ACTIONS if re.search(rf"\b{a}\b", text)]
    # The failsafe must name exactly one terminal action.
    return hits[0] if len(hits) == 1 else None


def parse(path: str | Path = DEFAULT_PATH) -> list[Policy]:
    """Parse and structurally validate the handbook. Raises HandbookError."""
    text = Path(path).read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise HandbookError(f"missing {START!r} / {END!r} markers")
    body = text.split(START, 1)[1].split(END, 1)[0]

    heads = list(_POLICY_HEAD.finditer(body))
    if not heads:
        raise HandbookError("no POLICY_ID blocks found")

    policies: list[Policy] = []
    seen_ids: set[str] = set()
    for i, head in enumerate(heads):
        policy_id = head.group(1)
        block_start = head.start()
        block_end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        block = body[block_start:block_end].strip()

        if policy_id in seen_ids:
            raise HandbookError(f"duplicate POLICY_ID {policy_id!r}")
        seen_ids.add(policy_id)

        fields = {}
        for key, rx in _FIELD.items():
            m = rx.search(block)
            if not m:
                pretty = key.replace("_", " ").title()
                raise HandbookError(f"{policy_id}: missing **{pretty}:** field")
            fields[key] = m.group(1).strip()

        if fields["status"] not in VALID_STATUS:
            raise HandbookError(
                f"{policy_id}: status {fields['status']!r} not in {sorted(VALID_STATUS)}")

        cp = _CORE_PROP.search(block)
        if not cp or not cp.group(1).strip():
            raise HandbookError(f"{policy_id}: missing '### 1. Plain English Core Property'")
        core_property = cp.group(1).strip()

        clauses: dict[str, str] = {}
        for m in _CLAUSE.finditer(block):
            cid, ctext = m.group(1), m.group(2).strip()
            if cid in clauses:
                raise HandbookError(f"{policy_id}: duplicate {cid}")
            clauses[cid] = ctext

        if not clauses:
            raise HandbookError(f"{policy_id}: no enumerated CLAUSE_n obligation clauses")

        # Clause ids must be sequential CLAUSE_1..CLAUSE_N (no gaps).
        expected = [f"CLAUSE_{n}" for n in range(1, len(clauses) + 1)]
        if list(clauses) != expected:
            raise HandbookError(
                f"{policy_id}: clause ids {list(clauses)} are not sequential {expected}")

        te = _TARGET_EXPLOIT.search(block)
        ef = _EXPECTED_FAIL.search(block)
        if not te or not ef:
            raise HandbookError(
                f"{policy_id}: Core Negative Vector missing Target Exploit / "
                "Expected System Failure Point")
        expected_action = _action_in(ef.group(1))
        if expected_action is None:
            raise HandbookError(
                f"{policy_id}: negative-vector expected action must name exactly one of "
                f"{sorted(VALID_ACTIONS)}")
        negative_vector = NegativeVector(te.group(1).strip(), expected_action)

        not_claims: dict[str, str] = {}
        for m in _NOT_CLAIM.finditer(block):
            nid, ntext = m.group(1), m.group(2).strip()
            if nid in not_claims:
                raise HandbookError(f"{policy_id}: duplicate {nid}")
            not_claims[nid] = ntext
        if not not_claims:
            raise HandbookError(f"{policy_id}: no Explicit NOT-Claims (validation horizon unbounded)")

        policies.append(Policy(
            policy_id=policy_id,
            threat_category=fields["threat_category"],
            incident_anchor=fields["incident_anchor"],
            status=fields["status"],
            core_property=core_property,
            clauses=clauses,
            negative_vector=negative_vector,
            not_claims=not_claims,
            raw_block=block))

    return policies


def by_id(policies: list[Policy], policy_id: str) -> Policy:
    for p in policies:
        if p.policy_id == policy_id:
            return p
    raise HandbookError(f"unknown POLICY_ID {policy_id!r}")


def extract_block(policy_id: str, path: str | Path = DEFAULT_PATH) -> str:
    """The verbatim markdown block for one policy — what the dispatch loop copies
    into /home/<agent>/spec.txt at delegation time (spec §1)."""
    return by_id(parse(path), policy_id).raw_block


if __name__ == "__main__":
    for p in parse():
        nv = p.negative_vector
        print(f"{p.policy_id}  [{p.status}]  {p.threat_category}")
        print(f"    clauses: {len(p.clauses)} ({', '.join(p.clause_ids)})")
        print(f"    negative vector -> expected action {nv.expected_action}")
        print(f"    NOT-claims: {len(p.not_claims)}")
