"""Parser + structural validator for the Upper Bound (textbook_manifest.md).

The manifest is the citable normative ceiling for Use Case D (Rocq) -- spec §2.
This module turns its strict, token-parsable Markdown into structured objects so
the orchestrator can:
  - dispatch one exercise's block into spec.txt at delegation time (§1),
  - assert at Gate A that a plan blueprint maps every CLAUSE_X (§3),
  - assert at Gate C that the exerciser's mutation matrix targets every CLAUSE_X (§3).

There is exactly one parser (this file); the manifest is authored to it, so a
malformed ceiling is a hard, early failure rather than a silently misread rule.

The clause ids, EXERCISE_ID key, and START/END markers are kept token-identical
to what the ground-truth `gate_sentinel.py` reads from the *deployed* manifest at
`/opt/squeeze/shared/textbook_manifest.md` (see ../ground-truth/shared/contract.md).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

START = "# TEXTBOOK_MANIFEST_START"
END = "# TEXTBOOK_MANIFEST_END"
VALID_STATUS = {"BINDING", "DRAFT", "DEPRECATED"}

DEFAULT_PATH = Path(__file__).resolve().parent / "textbook_manifest.md"


class ManifestError(ValueError):
    """Raised when the manifest violates its schema (spec §2)."""


@dataclass(frozen=True)
class Exercise:
    exercise_id: str
    textbook_reference: str
    domain: str
    status: str
    english_text: str
    scope_boundaries: list[str]
    clauses: dict[str, str]        # {"CLAUSE_1": text, ...}, insertion-ordered
    target_mutation: str           # the core negative vector
    expected_defense: str
    not_claims: dict[str, str]     # {"NOT_CLAIM_1": text, ...}
    raw_block: str                 # verbatim markdown for this exercise (for dispatch)

    @property
    def clause_ids(self) -> list[str]:
        return list(self.clauses)


_FIELD = {
    "textbook_reference": re.compile(r"\*\*Textbook Reference:\*\*\s*(.+)"),
    "domain": re.compile(r"\*\*Mathematical Domain:\*\*\s*(.+)"),
    "status": re.compile(r"\*\*Status:\*\*\s*(\S+)"),
}
_ENGLISH = re.compile(
    r"###\s*1\.\s*English Exercise Text\s*(.*?)(?=\n###\s*\d|\Z)", re.DOTALL)
_SCOPE = re.compile(r"\*\*Scope Boundary\s+\d+:\*\*\s*(.+)")
_CLAUSE = re.compile(r"\*\*(CLAUSE_\d+):\*\*\s*(.+)")
_TARGET_MUT = re.compile(r"\*\*Target Mutation:\*\*\s*(.+)")
_EXP_DEF = re.compile(r"\*\*Expected System Defense:\*\*\s*(.+)")
_NOT_CLAIM = re.compile(r"\*\*(NOT_CLAIM_\d+):\*\*\s*(.+)")
_EXERCISE_HEAD = re.compile(r"^##\s*EXERCISE_ID:\s*(\S+)\s*$", re.MULTILINE)


def parse(path: str | Path = DEFAULT_PATH) -> list[Exercise]:
    """Parse and structurally validate the manifest. Raises ManifestError."""
    text = Path(path).read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise ManifestError(f"missing {START!r} / {END!r} markers")
    body = text.split(START, 1)[1].split(END, 1)[0]

    heads = list(_EXERCISE_HEAD.finditer(body))
    if not heads:
        raise ManifestError("no EXERCISE_ID blocks found")

    exercises: list[Exercise] = []
    seen_ids: set[str] = set()
    for i, head in enumerate(heads):
        exercise_id = head.group(1)
        block_start = head.start()
        block_end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        block = body[block_start:block_end].strip()

        if exercise_id in seen_ids:
            raise ManifestError(f"duplicate EXERCISE_ID {exercise_id!r}")
        seen_ids.add(exercise_id)

        fields = {}
        for key, rx in _FIELD.items():
            m = rx.search(block)
            if not m:
                pretty = key.replace("_", " ").title()
                raise ManifestError(f"{exercise_id}: missing **{pretty}:** field")
            fields[key] = m.group(1).strip()

        if fields["status"] not in VALID_STATUS:
            raise ManifestError(
                f"{exercise_id}: status {fields['status']!r} not in {sorted(VALID_STATUS)}")

        em = _ENGLISH.search(block)
        if not em or not em.group(1).strip():
            raise ManifestError(f"{exercise_id}: missing English Exercise Text (schema §1)")
        english = em.group(1).strip()

        scope = [m.group(1).strip() for m in _SCOPE.finditer(block)]
        if not scope:
            raise ManifestError(
                f"{exercise_id}: no Scope Boundary bullets (the ceiling is unbounded)")

        clauses: dict[str, str] = {}
        for m in _CLAUSE.finditer(block):
            cid, ctext = m.group(1), m.group(2).strip()
            if cid in clauses:
                raise ManifestError(f"{exercise_id}: duplicate {cid}")
            clauses[cid] = ctext

        # Clause ids must be sequential CLAUSE_1..CLAUSE_N (no gaps), so Gate A/C
        # cannot silently lose a clause through a numbering hole.
        expected = [f"CLAUSE_{n}" for n in range(1, len(clauses) + 1)]
        if list(clauses) != expected:
            raise ManifestError(
                f"{exercise_id}: clause ids {list(clauses)} are not sequential {expected}")

        if fields["status"] == "BINDING" and not clauses:
            raise ManifestError(
                f"{exercise_id}: BINDING exercise has no obligation clauses "
                "(Gate A/C would be vacuous)")

        tm = _TARGET_MUT.search(block)
        if not tm:
            raise ManifestError(
                f"{exercise_id}: missing **Target Mutation:** (core negative vector, §4)")
        ed = _EXP_DEF.search(block)
        if not ed:
            raise ManifestError(
                f"{exercise_id}: missing **Expected System Defense:** (§4)")

        not_claims: dict[str, str] = {}
        for m in _NOT_CLAIM.finditer(block):
            nid, ntext = m.group(1), m.group(2).strip()
            if nid in not_claims:
                raise ManifestError(f"{exercise_id}: duplicate {nid}")
            not_claims[nid] = ntext
        if not not_claims:
            raise ManifestError(
                f"{exercise_id}: no NOT_CLAIM_X bullets (validation footprint unbounded, §5)")

        exercises.append(Exercise(
            exercise_id=exercise_id,
            textbook_reference=fields["textbook_reference"],
            domain=fields["domain"],
            status=fields["status"],
            english_text=english,
            scope_boundaries=scope,
            clauses=clauses,
            target_mutation=tm.group(1).strip(),
            expected_defense=ed.group(1).strip(),
            not_claims=not_claims,
            raw_block=block))

    return exercises


def by_id(exercises: list[Exercise], exercise_id: str) -> Exercise:
    for e in exercises:
        if e.exercise_id == exercise_id:
            return e
    raise ManifestError(f"unknown EXERCISE_ID {exercise_id!r}")


def extract_block(exercise_id: str, path: str | Path = DEFAULT_PATH) -> str:
    """The verbatim markdown block for one exercise -- what the dispatch loop
    copies into /home/<agent>/spec.txt at delegation time (spec §1)."""
    return by_id(parse(path), exercise_id).raw_block


if __name__ == "__main__":
    for e in parse():
        print(f"{e.exercise_id}  [{e.status}]  {e.domain}  "
              f"({len(e.clauses)} clauses, {len(e.scope_boundaries)} bounds, "
              f"{len(e.not_claims)} NOT-claims)")
        print(f"    target mutation: {e.target_mutation}")
