#!/usr/bin/env python3
"""Document-plane compute engine (spec §2 Plane 1).

A pinned, local, stdlib-only OpenAPI-style schema linter. The document track uses
it to validate that a contract file conforms to the structural rules: well-formed
JSON, every route declares its methods, every method has typed request/response
schemas, documents its error responses (400/401/404 as applicable), and carries
no blank required descriptions or invalid structural nesting. It aborts (nonzero
exit) on a malformed or incomplete schema.

This is what validates `base_schema.json` (the canonical contract) and, later, the
implementer's `openapi.json`.

Usage:  python3 linter.py <schema.json>
Exit:   0 = conformant; 1 = lint errors (printed); 2 = file/JSON unreadable.
"""

import json
import sys
from pathlib import Path

# Statuses every operation MUST document. 2xx is the success payload; 401 is the
# auth failure; 404 the unknown-route failure. A mutating (POST) operation must
# also document 400 for a malformed body.
REQUIRED_STATUSES_ALL = ("401", "404")
SUCCESS_STATUSES = ("200",)
MUTATION_METHODS = ("post", "put", "patch", "delete")
HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")
ERROR_REQUIRED_PROPS = ("error", "message")


def _is_typed_object_schema(schema):
    """A schema must be an object with `type`, and if it is an object type it must
    declare `properties`. Every property must declare a `type`."""
    if not isinstance(schema, dict):
        return False, "schema is not an object"
    if "type" not in schema:
        return False, "schema missing 'type'"
    if schema["type"] == "object":
        props = schema.get("properties")
        if not isinstance(props, dict) or not props:
            return False, "object schema missing non-empty 'properties'"
        for pname, pspec in props.items():
            if not isinstance(pspec, dict) or "type" not in pspec:
                return False, f"property '{pname}' missing 'type'"
            desc = pspec.get("description")
            if "description" in pspec and (not isinstance(desc, str) or desc.strip() == ""):
                return False, f"property '{pname}' has a blank description"
    return True, ""


def lint(schema, errors):
    if not isinstance(schema, dict):
        errors.append("top-level schema is not a JSON object")
        return
    paths = schema.get("paths")
    if not isinstance(paths, dict) or not paths:
        errors.append("schema has no non-empty 'paths' object")
        return

    for path, ops in sorted(paths.items()):
        if not isinstance(ops, dict) or not ops:
            errors.append(f"{path}: no methods declared")
            continue
        method_seen = False
        for method, op in sorted(ops.items()):
            ml = method.lower()
            if ml not in HTTP_METHODS:
                continue
            method_seen = True
            where = f"{path} [{ml.upper()}]"

            if not isinstance(op, dict):
                errors.append(f"{where}: operation is not an object")
                continue

            # description on the operation must be present and non-blank
            desc = op.get("description")
            if not isinstance(desc, str) or desc.strip() == "":
                errors.append(f"{where}: missing or blank operation description")

            # mutations must declare a typed request body schema
            if ml in MUTATION_METHODS:
                rb = op.get("requestBody")
                if not isinstance(rb, dict) or "schema" not in rb:
                    errors.append(f"{where}: mutation lacks a requestBody.schema")
                else:
                    ok, why = _is_typed_object_schema(rb["schema"])
                    if not ok:
                        errors.append(f"{where}: requestBody.schema invalid -- {why}")

            responses = op.get("responses")
            if not isinstance(responses, dict) or not responses:
                errors.append(f"{where}: no responses declared")
                continue

            # required statuses: success + 401 + 404 (+ 400 for mutations)
            required = list(SUCCESS_STATUSES) + list(REQUIRED_STATUSES_ALL)
            if ml in MUTATION_METHODS:
                required.append("400")
            for status in required:
                if status not in responses:
                    errors.append(f"{where}: missing documented response {status}")

            for status, resp in sorted(responses.items()):
                if not isinstance(resp, dict):
                    errors.append(f"{where} {status}: response is not an object")
                    continue
                rdesc = resp.get("description")
                if not isinstance(rdesc, str) or rdesc.strip() == "":
                    errors.append(f"{where} {status}: blank response description")
                rschema = resp.get("schema")
                ok, why = _is_typed_object_schema(rschema)
                if not ok:
                    errors.append(f"{where} {status}: response schema invalid -- {why}")
                    continue
                # error responses must declare error+message
                if status[0] in ("4", "5"):
                    props = rschema.get("properties", {})
                    req = rschema.get("required", [])
                    for needed in ERROR_REQUIRED_PROPS:
                        if needed not in props or needed not in req:
                            errors.append(
                                f"{where} {status}: error payload must require "
                                f"'{needed}'")
        if not method_seen:
            errors.append(f"{path}: no valid HTTP methods declared")


def lint_file(path):
    """Return list of error strings ([] == clean). Raises on unreadable JSON."""
    text = Path(path).read_text()
    schema = json.loads(text)  # raises ValueError on malformed JSON
    errors = []
    lint(schema, errors)
    return errors


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: python3 linter.py <schema.json>", file=sys.stderr)
        return 2
    path = argv[0]
    try:
        errors = lint_file(path)
    except FileNotFoundError:
        print(f"error: schema file not found: {path}", file=sys.stderr)
        return 2
    except ValueError as e:
        print(f"error: {path} is not well-formed JSON: {e}", file=sys.stderr)
        return 2

    if errors:
        print(f"LINT FAILED: {path} ({len(errors)} problem(s))")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"LINT OK: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
