"""Parser + structural validator for the Upper Bound (api_policy_manifest.md).

The manifest is the citable normative ceiling (spec §2). This module turns its
strict, token-parsable Markdown into structured objects so the orchestrator can:
  - dispatch one manifest's block into spec.txt at delegation time (§1),
  - assert at Gate A that the file stays policy-centric (no code/schema/impl),
  - assert at Gate C that the exerciser's matrix covers every CLAUSE_X (§3).

There is exactly one parser (this file); the manifest is authored to it, so a
malformed ceiling is a hard, early failure rather than a silently misread rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

START = "# API_POLICY_MANIFEST_START"
END = "# API_POLICY_MANIFEST_END"
VALID_STATUS = {"BINDING", "DRAFT", "DEPRECATED"}

DEFAULT_PATH = Path(__file__).resolve().parent / "api_policy_manifest.md"


class HandbookError(ValueError):
    """Raised when the manifest violates its schema (spec §2)."""


@dataclass(frozen=True)
class NegativeVector:
    target_exploit: str
    expected_defense: str        # the mandated safe response, verbatim


@dataclass(frozen=True)
class Manifest:
    manifest_id: str
    architecture_category: str
    interface_scope: str
    status: str
    core_property: str
    clauses: dict[str, str]            # {"CLAUSE_1": text, ...}, insertion-ordered
    negative_vector: NegativeVector
    not_claims: dict[str, str]         # {"NOT_CLAIM_1": text, ...}
    raw_block: str                     # verbatim markdown for this manifest (for dispatch)

    @property
    def clause_ids(self) -> list[str]:
        return list(self.clauses)


_FIELD = {
    "architecture_category": re.compile(r"\*\*Architecture Category:\*\*\s*(.+)"),
    "interface_scope": re.compile(r"\*\*Target Interface Scope:\*\*\s*(.+)"),
    "status": re.compile(r"\*\*Status:\*\*\s*(\S+)"),
}
_MANIFEST_HEAD = re.compile(r"^##\s*MANIFEST_ID:\s*(\S+)\s*$", re.MULTILINE)
_CLAUSE = re.compile(r"\*\*(CLAUSE_\d+):\*\*\s*(.+)")
_NOT_CLAIM = re.compile(r"\*\*(NOT_CLAIM_\d+):\*\*\s*(.+)")
_CORE_PROP = re.compile(
    r"###\s*1\.\s*Plain English Core Property\s*\n(.*?)(?=\n###\s|\Z)", re.DOTALL)
_TARGET_EXPLOIT = re.compile(r"\*\*Target Exploit:\*\*\s*(.+)")
_EXPECTED_DEFENSE = re.compile(r"\*\*Expected System Defense:\*\*\s*(.+)")


def parse(path: str | Path = DEFAULT_PATH) -> list[Manifest]:
    """Parse and structurally validate the manifest. Raises HandbookError."""
    text = Path(path).read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise HandbookError(f"missing {START!r} / {END!r} markers")
    body = text.split(START, 1)[1].split(END, 1)[0]

    heads = list(_MANIFEST_HEAD.finditer(body))
    if not heads:
        raise HandbookError("no MANIFEST_ID blocks found")

    manifests: list[Manifest] = []
    seen_ids: set[str] = set()
    for i, head in enumerate(heads):
        manifest_id = head.group(1)
        block_start = head.start()
        block_end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        block = body[block_start:block_end].strip()

        if manifest_id in seen_ids:
            raise HandbookError(f"duplicate MANIFEST_ID {manifest_id!r}")
        seen_ids.add(manifest_id)

        fields = {}
        for key, rx in _FIELD.items():
            m = rx.search(block)
            if not m:
                pretty = key.replace("_", " ").title()
                raise HandbookError(f"{manifest_id}: missing **{pretty}:** field")
            fields[key] = m.group(1).strip()

        if fields["status"] not in VALID_STATUS:
            raise HandbookError(
                f"{manifest_id}: status {fields['status']!r} not in {sorted(VALID_STATUS)}")

        cp = _CORE_PROP.search(block)
        if not cp or not cp.group(1).strip():
            raise HandbookError(f"{manifest_id}: missing '### 1. Plain English Core Property'")
        core_property = cp.group(1).strip()

        clauses: dict[str, str] = {}
        for m in _CLAUSE.finditer(block):
            cid, ctext = m.group(1), m.group(2).strip()
            if cid in clauses:
                raise HandbookError(f"{manifest_id}: duplicate {cid}")
            clauses[cid] = ctext

        if not clauses:
            raise HandbookError(f"{manifest_id}: no enumerated CLAUSE_n obligation clauses")

        # Clause ids must be sequential CLAUSE_1..CLAUSE_N (no gaps).
        expected = [f"CLAUSE_{n}" for n in range(1, len(clauses) + 1)]
        if list(clauses) != expected:
            raise HandbookError(
                f"{manifest_id}: clause ids {list(clauses)} are not sequential {expected}")

        te = _TARGET_EXPLOIT.search(block)
        ef = _EXPECTED_DEFENSE.search(block)
        if not te or not ef:
            raise HandbookError(
                f"{manifest_id}: Core Negative Vector missing Target Exploit / "
                "Expected System Defense")
        negative_vector = NegativeVector(te.group(1).strip(), ef.group(1).strip())

        not_claims: dict[str, str] = {}
        for m in _NOT_CLAIM.finditer(block):
            nid, ntext = m.group(1), m.group(2).strip()
            if nid in not_claims:
                raise HandbookError(f"{manifest_id}: duplicate {nid}")
            not_claims[nid] = ntext
        if not not_claims:
            raise HandbookError(
                f"{manifest_id}: no Explicit NOT-Claims (validation horizon unbounded)")

        manifests.append(Manifest(
            manifest_id=manifest_id,
            architecture_category=fields["architecture_category"],
            interface_scope=fields["interface_scope"],
            status=fields["status"],
            core_property=core_property,
            clauses=clauses,
            negative_vector=negative_vector,
            not_claims=not_claims,
            raw_block=block))

    return manifests


def by_id(manifests: list[Manifest], manifest_id: str) -> Manifest:
    for m in manifests:
        if m.manifest_id == manifest_id:
            return m
    raise HandbookError(f"unknown MANIFEST_ID {manifest_id!r}")


def extract_block(manifest_id: str, path: str | Path = DEFAULT_PATH) -> str:
    """The verbatim markdown block for one manifest — what the dispatch loop copies
    into /home/<agent>/spec.txt at delegation time (spec §1)."""
    return by_id(parse(path), manifest_id).raw_block


if __name__ == "__main__":
    for m in parse():
        nv = m.negative_vector
        print(f"{m.manifest_id}  [{m.status}]  {m.architecture_category}")
        print(f"    scope: {m.interface_scope}")
        print(f"    clauses: {len(m.clauses)} ({', '.join(m.clause_ids)})")
        print(f"    negative vector -> {nv.target_exploit[:60]}...")
        print(f"    NOT-claims: {len(m.not_claims)}")
