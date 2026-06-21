"""Parser + structural validator for the Upper Bound (metric_handbook.md).

The handbook is the citable normative ceiling (spec §2). This module turns its
strict, token-parsable Markdown into structured objects so the orchestrator can:
  - dispatch one metric's block into spec.txt at delegation time (§1),
  - assert at Gate A that a plan cites every CLAUSE_X (§3),
  - assert at Gate C that the exerciser's assertions cover every CLAUSE_X (§3).

There is exactly one parser (this file); the handbook is authored to it, so a
malformed ceiling is a hard, early failure rather than a silently misread rule.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

START = "# METRIC_HANDBOOK_START"
END = "# METRIC_HANDBOOK_END"
VALID_STATUS = {"BINDING", "DRAFT", "DEPRECATED"}

DEFAULT_PATH = Path(__file__).resolve().parent / "metric_handbook.md"


class HandbookError(ValueError):
    """Raised when the handbook violates its schema (spec §2)."""


@dataclass(frozen=True)
class Metric:
    metric_id: str
    name: str
    status: str
    target_table: str
    formula: str
    exclusions: list[str]
    clauses: dict[str, str]   # {"CLAUSE_1": text, ...}, insertion-ordered
    raw_block: str            # the verbatim markdown for this metric (for dispatch)

    @property
    def clause_ids(self) -> list[str]:
        return list(self.clauses)


_FIELD = {
    "name": re.compile(r"\*\*Name:\*\*\s*(.+)"),
    "status": re.compile(r"\*\*Status:\*\*\s*(\S+)"),
    "target_table": re.compile(r"\*\*Target Table:\*\*\s*`?([A-Za-z_][A-Za-z0-9_]*)`?"),
}
_FORMULA = re.compile(r"###\s*1\.\s*Normative Formula\s*```[a-z]*\n(.*?)```", re.DOTALL)
_EXCLUSION = re.compile(r"\*\*Exclusion\s+\d+:\*\*\s*(.+)")
_CLAUSE = re.compile(r"\*\*(CLAUSE_\d+):\*\*\s*(.+)")
_METRIC_HEAD = re.compile(r"^##\s*METRIC_ID:\s*(\S+)\s*$", re.MULTILINE)


def parse(path: str | Path = DEFAULT_PATH) -> list[Metric]:
    """Parse and structurally validate the handbook. Raises HandbookError."""
    text = Path(path).read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise HandbookError(f"missing {START!r} / {END!r} markers")
    body = text.split(START, 1)[1].split(END, 1)[0]

    heads = list(_METRIC_HEAD.finditer(body))
    if not heads:
        raise HandbookError("no METRIC_ID blocks found")

    metrics: list[Metric] = []
    seen_ids: set[str] = set()
    for i, head in enumerate(heads):
        metric_id = head.group(1)
        block_start = head.start()
        block_end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        block = body[block_start:block_end].strip()

        if metric_id in seen_ids:
            raise HandbookError(f"duplicate METRIC_ID {metric_id!r}")
        seen_ids.add(metric_id)

        fields = {}
        for key, rx in _FIELD.items():
            m = rx.search(block)
            if not m:
                raise HandbookError(f"{metric_id}: missing **{key.replace('_', ' ').title()}:** field")
            fields[key] = m.group(1).strip()

        if fields["status"] not in VALID_STATUS:
            raise HandbookError(f"{metric_id}: status {fields['status']!r} not in {sorted(VALID_STATUS)}")

        fm = _FORMULA.search(block)
        if not fm:
            raise HandbookError(f"{metric_id}: missing or malformed Normative Formula code block")
        formula = fm.group(1).strip()

        exclusions = [m.group(1).strip() for m in _EXCLUSION.finditer(block)]

        clauses: dict[str, str] = {}
        for m in _CLAUSE.finditer(block):
            cid, ctext = m.group(1), m.group(2).strip()
            if cid in clauses:
                raise HandbookError(f"{metric_id}: duplicate {cid}")
            clauses[cid] = ctext

        # Clause ids must be sequential CLAUSE_1..CLAUSE_N (no gaps).
        expected = [f"CLAUSE_{n}" for n in range(1, len(clauses) + 1)]
        if list(clauses) != expected:
            raise HandbookError(
                f"{metric_id}: clause ids {list(clauses)} are not sequential {expected}")

        if fields["status"] == "BINDING" and not clauses:
            raise HandbookError(f"{metric_id}: BINDING metric has no obligation clauses (Gate C would be vacuous)")

        metrics.append(Metric(
            metric_id=metric_id, name=fields["name"], status=fields["status"],
            target_table=fields["target_table"], formula=formula,
            exclusions=exclusions, clauses=clauses, raw_block=block))

    return metrics


def by_id(metrics: list[Metric], metric_id: str) -> Metric:
    for m in metrics:
        if m.metric_id == metric_id:
            return m
    raise HandbookError(f"unknown METRIC_ID {metric_id!r}")


def extract_block(metric_id: str, path: str | Path = DEFAULT_PATH) -> str:
    """The verbatim markdown block for one metric — what the dispatch loop copies
    into /home/<agent>/spec.txt at delegation time (spec §1)."""
    return by_id(parse(path), metric_id).raw_block


if __name__ == "__main__":
    for m in parse():
        print(f"{m.metric_id}  [{m.status}]  {m.name}  -> {m.target_table}  "
              f"({len(m.clauses)} clauses, {len(m.exclusions)} exclusions)")
