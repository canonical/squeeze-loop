#!/usr/bin/env python3
"""
sl2plantuml — validate a Squeeze-Loop (SL 1.0) JSON document against its schema,
then either emit the PlantUML source or render it to a PNG.

Usage:
    sl2plantuml.py LOOP.json                 # validate, then render LOOP.png
    sl2plantuml.py LOOP.json --plant out.puml  # validate, then write PlantUML source
    sl2plantuml.py LOOP.json -o diagram.png  # validate, then render to a chosen path
    sl2plantuml.py LOOP.json --direction tb  # top-to-bottom layout (clearer for dense loops)
    sl2plantuml.py LOOP.json --svg           # render LOOP.svg (scalable vector) instead of PNG
    sl2plantuml.py LOOP.json -o docs/img/LOOP.png   # convention: rendered images live in docs/img/

Convention: write rendered images to `docs/img/` (PNG and SVG), so a loop's companion
`docs/<id>.md` embeds them as `img/<id>.svg`.

Rendering shells out to `plantuml` (which needs Java + Graphviz). Validation needs
the `jsonschema` package:  pip install jsonschema
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------- #
#  Visual mapping (matches the slide legend)
# --------------------------------------------------------------------------- #
ACTOR_COLOR = "#E8541E"          # agents
DEFAULT_SOURCE_COLOR = "#E2E2E2"  # fallback / artifact grey
SOURCE_COLORS = {
    "soft_authority":    "#C9E7CB",  # upper-bound material  (green)
    "executable_oracle": "#F3CBD0",  # runnable oracle       (pink)
    "artifact":          "#E2E2E2",  # produced / under test (grey)
    "rationale":         "#F4CCCC",  # must-not-see material  (light red)
    "human_judgment":    "#D9D2E9",  # terminus judgment     (lavender)
}

LEGEND = "\n".join([
    "legend right",
    "|= Colour |= Meaning |",
    "|<#E8541E>| Agent (actor) |",
    "|<#C9E7CB>| Upper-bound material |",
    "|<#F3CBD0>| Executable oracle |",
    "|<#E2E2E2>| Artifact |",
    "|<#F4CCCC>| Rationale (must-not-see) |",
    "|<#D9D2E9>| Human judgment |",
    "endlegend",
])


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def die(msg: str, code: int = 2) -> "NoReturn":  # type: ignore[name-defined]
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(code)


def _alias(prefix: str, ident: str) -> str:
    """A PlantUML-safe alias. Actors and sources are namespaced so their ids
    can never collide even if the two registries reuse a string."""
    return prefix + re.sub(r"\W", "_", ident)


def _esc(text: str) -> str:
    """Escape a quoted PlantUML label."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


# --------------------------------------------------------------------------- #
#  Schema validation
# --------------------------------------------------------------------------- #
def load_schema() -> dict:
    return json.loads(SCHEMA_JSON)


def validate(doc: dict) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        die("the 'jsonschema' package is required for validation.\n"
            "       install it with:  pip install jsonschema")

    validator = Draft202012Validator(load_schema())
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        print("schema validation FAILED:", file=sys.stderr)
        for e in errors:
            loc = "/".join(str(p) for p in e.path) or "(root)"
            print(f"  • {loc}: {e.message}", file=sys.stderr)
        sys.exit(1)
    print("schema validation: OK")


# --------------------------------------------------------------------------- #
#  PlantUML generation
# --------------------------------------------------------------------------- #
DIRECTIVE = {"lr": "left to right direction", "tb": "top to bottom direction"}


def to_plantuml(doc: dict, direction: str = "lr") -> tuple[str, list[str]]:
    actors = doc.get("actors", []) or []
    sources = doc.get("sources", []) or []
    source_ids = {s["id"] for s in sources}
    actor_ids = {a["id"] for a in actors}
    warnings: list[str] = []

    def a_alias(i: str) -> str:
        return _alias("A_", i)

    def s_alias(i: str) -> str:
        return _alias("S_", i)

    out: list[str] = []
    out.append(f'@startuml {doc.get("id", "sl")}')
    title = doc.get("id", "squeeze-loop")
    kind = doc.get("kind")
    out.append(f"title {title}" + (f" ({kind})" if kind else ""))
    out.append(DIRECTIVE[direction])
    out.append("skinparam rectangleBorderColor #555")
    out.append("skinparam shadowing false")
    out.append("")

    # --- nodes: actors -----------------------------------------------------
    out.append("' --- actors (agents) ---")
    for a in actors:
        out.append(f'rectangle "{_esc(a["name"])}" as {a_alias(a["id"])} {ACTOR_COLOR}')
    out.append("")

    # --- nodes: sources ----------------------------------------------------
    out.append("' --- sources ---")
    for s in sources:
        color = SOURCE_COLORS.get(s.get("type"), DEFAULT_SOURCE_COLOR)
        out.append(f'rectangle "{_esc(s["name"])}" as {s_alias(s["id"])} {color}')
    out.append("")

    def bound_edge(actor_id: str, sid: str, style: str, label: str) -> None:
        if sid not in source_ids:
            warnings.append(f'actor "{actor_id}" references unknown source "{sid}"')
            return
        out.append(f"{a_alias(actor_id)} {style} {s_alias(sid)} : {label}")

    # --- edges: bounds + production ---------------------------------------
    out.append("' --- bounds (U / L) and production ---")
    for a in actors:
        aid = a["id"]
        for sid in (a.get("upper_bound", {}) or {}).get("sources", []) or []:
            bound_edge(aid, sid, "-->", "U")
        for sid in (a.get("lower_bound", {}) or {}).get("sources", []) or []:
            bound_edge(aid, sid, "-->", "L")
        for sid in a.get("produces", []) or []:
            bound_edge(aid, sid, "..>", "produces")
    out.append("")

    # --- edges: must-not-see barriers -------------------------------------
    out.append("' --- must-not-see barriers ---")
    for a in actors:
        for sid in a.get("must_not_see", []) or []:
            if sid not in source_ids:
                warnings.append(f'actor "{a["id"]}" must_not_see unknown source "{sid}"')
                continue
            out.append(f"{a_alias(a['id'])} -[#red,dashed]-> {s_alias(sid)} : \u2717 must not see")
    out.append("")

    # --- edges: catchability (the squeeze) --------------------------------
    out.append("' --- catchability (the squeeze) ---")
    for c in (doc.get("disjointness", {}) or {}).get("catchability", []) or []:
        caught, catcher = c.get("actor"), c.get("caught_by")
        if caught not in actor_ids or catcher not in actor_ids:
            warnings.append(f'catchability references unknown actor(s): {catcher} -> {caught}')
            continue
        out.append(f"{a_alias(catcher)} -[#blue]-> {a_alias(caught)} : catches")
    out.append("")

    out.append(LEGEND)
    out.append("@enduml")
    return "\n".join(out), warnings


# --------------------------------------------------------------------------- #
#  Rendering (PNG / SVG)
# --------------------------------------------------------------------------- #
RENDER_FLAG = {"png": "-tpng", "svg": "-tsvg"}


def render(puml: str, out_path: Path, fmt: str = "png") -> None:
    plantuml = shutil.which("plantuml")
    if not plantuml:
        die("'plantuml' was not found on PATH.\n"
            "       install it (needs Java + Graphviz), e.g.:\n"
            "         Debian/Ubuntu : sudo apt install plantuml\n"
            "         macOS (brew)  : brew install plantuml\n"
            "       or download plantuml.jar and wrap it in a 'plantuml' shim.")
    proc = subprocess.run(
        [plantuml, RENDER_FLAG[fmt], "-charset", "UTF-8", "-pipe"],
        input=puml.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0 or not proc.stdout:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        die("plantuml failed to render:\n" + (detail or "(no stderr)"))
    out_path.write_bytes(proc.stdout)
    print(f"wrote {fmt.upper()} → {out_path}")


# --------------------------------------------------------------------------- #
#  CLI
# --------------------------------------------------------------------------- #
def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Validate an SL 1.0 JSON loop, then emit PlantUML or render a PNG.")
    parser.add_argument("json_file", type=Path, help="the SL 1.0 JSON document")
    parser.add_argument("--plant", metavar="FILE", type=Path,
                        help="write PlantUML source to FILE instead of rendering a PNG")
    parser.add_argument("-o", "--output", metavar="FILE", type=Path,
                        help="image output path (default: <input>.png, or .svg with --svg)")
    parser.add_argument("--svg", action="store_true",
                        help="render SVG (scalable vector) instead of PNG")
    parser.add_argument("--direction", choices=("lr", "tb"), default="lr",
                        help="layout orientation: lr = left-to-right (default), "
                             "tb = top-to-bottom (clearer for large, dense loops)")
    args = parser.parse_args(argv)

    if not args.json_file.is_file():
        die(f"no such file: {args.json_file}")
    try:
        doc = json.loads(args.json_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        die(f"{args.json_file} is not valid JSON: {e}")

    validate(doc)

    puml, warnings = to_plantuml(doc, direction=args.direction)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)

    if args.plant:
        args.plant.write_text(puml + "\n", encoding="utf-8")
        print(f"wrote PlantUML → {args.plant}")
    else:
        fmt = "svg" if args.svg else "png"
        out_path = args.output or args.json_file.with_suffix("." + fmt)
        render(puml, out_path, fmt)


# --------------------------------------------------------------------------- #
#  Embedded SL 1.0 schema  (so the tool is self-contained)
# --------------------------------------------------------------------------- #
SCHEMA_JSON = r'''{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/sl/sl-schema-1.0.json",
  "title": "Squeeze Loop (SL) \u2014 compact standardized representation",
  "description": "A machine-checkable encoding of a single squeeze loop. The load-bearing idea: every source of truth has a stable id, and each actor references sources by id in its bounds and barriers, so disjointness (C1), barrier consistency (C3) and endogeneity become set operations a tool can run.",
  "type": "object",
  "required": ["sl_version","id","kind","description","sources","actors","disjointness"],
  "additionalProperties": false,
  "properties": {
    "sl_version": {"const": "1.0"},
    "id": {"type": "string","pattern": "^[a-z0-9][a-z0-9-]*$","description": "Stable slug for the loop, e.g. 'my-loop'."},
    "kind": {"enum": ["base","monitor","meta"],"description": "base = produces a deliverable through a cast; monitor = squeezes another loop's soft outputs (sl-monitoring-sl); meta = an audit methodology with no 5-actor cast (sl-auditor)."},
    "description": {"type": "string","description": "One short paragraph: what the loop delivers and the dominant coherent-and-wrong it guards."},
    "terrain": {"type": "array","items": {"enum": ["A","B","C"]},"description": "Terrain archetype(s): A transcription / B authored authority / C split planes."},
    "monitors": {"type": ["string","null"],"description": "For kind=monitor/meta: the id of the loop this one observes (null otherwise)."},
    "sources": {"type": "array","minItems": 1,"description": "The registry of every source of truth, artifact, oracle, rationale and terminus in the loop. This registry is what makes disjointness checkable.","items": {"$ref": "#/$defs/source"}},
    "actors": {"type": "array","minItems": 1,"description": "The rows of the compact table, one object per actor.","items": {"$ref": "#/$defs/actor"}},
    "disjointness": {"$ref": "#/$defs/disjointness"}
  },
  "$defs": {
    "source": {
      "type": "object",
      "required": ["id","name","type"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string","pattern": "^[a-z0-9][a-z0-9_.-]*$"},
        "name": {"type": "string","description": "Human-readable name as it appears in the prose tables."},
        "type": {"enum": ["soft_authority","executable_oracle","artifact","rationale","human_judgment"],"description": "soft_authority = U-material (spec/standard/policy). executable_oracle = L-material (runnable, interpretation-free). artifact = a thing produced or under test (impl, contracts, tests). rationale = a producer's private reasoning (a judge must never read it). human_judgment = a terminus judgment, no executable oracle."},
        "provenance": {"enum": ["exogenous","endogenous","authored","external_tool","human","internal"],"description": "exogenous = independent of the artifact under test (gold). endogenous = read off the artifact under test (a disjointness violation at the bound level; a PASS against it is only self-consistency). authored = an upstream-authored U (terrain B). external_tool = a prover/checker/runtime. human = a human terminus. internal = produced inside this loop (set automatically by produced_by)."},
        "produced_by": {"type": ["string","null"],"description": "actor id that creates this source inside the loop, or null if it enters from outside. Drives the self-certification check: no actor may judge against a source it produced."},
        "executable": {"type": "boolean","description": "True only for sources whose verdict is mechanical and re-runnable."},
        "notes": {"type": "string"}
      }
    },
    "bound": {
      "type": "object",
      "description": "An (upper or lower) bound: prose + the set of source ids it rests on.",
      "required": ["text","sources"],
      "additionalProperties": false,
      "properties": {
        "text": {"type": "string","description": "The bound as written in the compact table."},
        "sources": {"type": "array","items": {"type": "string"},"description": "ids into sources[] this bound reads from. EMPTY + absent_reason set => a terminus with no executable L."},
        "executable": {"type": "boolean","description": "For L: is this bound a runnable oracle?"},
        "borrowed_from": {"type": ["string","null"],"description": "For monitor/meta loops whose bound IS the observed loop's bound: the observed loop id."},
        "absent_reason": {"type": ["string","null"],"description": "If sources is empty: why (e.g. 'no executable oracle \u2014 that absence is why it is the terminus')."}
      }
    },
    "actor": {
      "type": "object",
      "required": ["id","name","role","builds","upper_bound","lower_bound","forbidden_moves","must_not_see"],
      "additionalProperties": false,
      "properties": {
        "id": {"type": "string","pattern": "^[a-z0-9][a-z0-9_.-]*$"},
        "name": {"type": "string"},
        "role": {"enum": ["coordinator","property_author","implementer","exerciser","probe","human_terminus","monitor","sub_loop","auditor","disjoint_base","other"],"description": "Canonical cast plus the meta/monitor roles. human_terminus / disjoint_base carry no executable L. monitor borrows the observed loop's bounds. sub_loop is a bridge row: an entire base loop collapsed to one row."},
        "optional": {"type": "boolean","default": false},
        "builds": {"type": "string","description": "The 'Builds' row \u2014 the deliverable this actor produces."},
        "produces": {"type": "array","items": {"type": "string"},"description": "source ids this actor authors (must match sources[].produced_by). Used by the self-certification check."},
        "upper_bound": {"$ref": "#/$defs/bound"},
        "lower_bound": {"$ref": "#/$defs/bound"},
        "forbidden_moves": {"type": "array","items": {"type": "string"},"description": "The role-crossing actions that would relieve this actor's own pressure."},
        "must_not_see": {"type": "array","items": {"type": "string"},"description": "source ids that must be ABSENT from this actor's context (physical barrier, not honorary). A judge runs an oracle over an artifact; it never reads the artifact in must_not_see."},
        "invokes": {"type": ["object","null"],"additionalProperties": false,"description": "For a borrowed/invoked actor (e.g. the skill sub-monitor = the sl-monitoring-sl Monitor row, invoked not re-derived).","properties": {"loop": {"type": "string"},"row": {"type": "string"}}},
        "expands_to": {"type": ["string","null"],"description": "For a bridge row: the loop id this single row collapses (e.g. 'base-loop' inside its monitor). Its real cast lives in that loop's own document."}
      }
    },
    "disjointness": {
      "type": "object",
      "required": ["rationale","load_bearing_barrier","catchability"],
      "additionalProperties": false,
      "properties": {
        "rationale": {"type": "string","description": "The 'at a glance' prose: why no actor can certify its own work."},
        "load_bearing_barrier": {"type": "string","description": "The one separation the whole loop rests on."},
        "catchability": {"type": "array","description": "C2 made explicit: for each actor's characteristic blind spot, the OTHER actor that catches it.","items": {"type": "object","required": ["actor","blind_spot","caught_by"],"additionalProperties": false,"properties": {"actor": {"type": "string"},"blind_spot": {"type": "string"},"caught_by": {"type": "string","description": "actor id of the catcher (must differ from 'actor')."},"via": {"type": "string"}}}},
        "endogeneity_flags": {"type": "array","items": {"type": "string"},"description": "Sources/actors where U is endogenous: a PASS there certifies self-consistency, not conformance. Empty = none."},
        "terminus": {"type": ["string","null"],"description": "For soft-side loops: who supplies the human/cross-provider close (the disjoint base). null for fully mechanical loops."}
      }
    }
  }
}'''


if __name__ == "__main__":
    main()
