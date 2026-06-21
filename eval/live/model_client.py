#!/usr/bin/env python3
"""Pluggable model client for the live-model harness.

The repository ships NO API key (by design: live-model results are non-deterministic and
are never folded into the deterministic gates). Two backends, selected by environment:

  - Anthropic (default): runs when the `anthropic` SDK is installed and `ANTHROPIC_API_KEY`
    is set. The same-provider family as the paper's author.
  - Ollama (cross-provider): set `OLLAMA_HOST` (e.g. http://localhost:11434) and
    `CROSS_MODEL` (e.g. qwen3.6:27b-mlx). This is a GENUINELY cross-provider cast --
    independent pretraining from the Anthropic author -- which is the data point review8 asks
    for on the disjointness-of-evidence claim. One non-Anthropic model in the cast moves the
    claim from "owed" to "preliminary but real". Still non-deterministic, still logged-not-gated.

Until a backend is reachable `available()` reports why, and the harness skips cleanly (never
fabricates). Keep it ONE call per invocation -- per-task independence is the rigor upgrade in
the plan; the harness handles repetition, seeding, and scoring.
"""
import json
import os
import urllib.request

# tier labels (the harness's --tiers axis) -> concrete model ids, weak -> strong.
# Edit to the models you want on the gradient. (Anthropic backend only; for the Ollama
# backend every tier resolves to CROSS_MODEL -- one cross-provider model, the cast's point.)
TIER_MODELS = {
    "weak":   "claude-haiku-4-5",
    "mid":    "claude-sonnet-4-6",
    "strong": "claude-opus-4-8",
}

OLLAMA_HOST = (os.environ.get("OLLAMA_HOST") or "").rstrip("/")
CROSS_MODEL = os.environ.get("CROSS_MODEL")

_client = None


class ModelClientUnset(Exception):
    pass


def _backend():
    """Ollama if OLLAMA_HOST is set (the cross-provider cast); else Anthropic."""
    return "ollama" if OLLAMA_HOST else "anthropic"


def available():
    """(ok, reason) -- check prerequisites WITHOUT making a generation call."""
    if _backend() == "ollama":
        if not CROSS_MODEL:
            return (False, "OLLAMA_HOST set but CROSS_MODEL not set (e.g. qwen3.6:27b-mlx)")
        try:
            with urllib.request.urlopen(f"{OLLAMA_HOST}/api/tags", timeout=8):
                pass
        except Exception as e:
            return (False, f"ollama at {OLLAMA_HOST} unreachable ({e})")
        return (True, f"ollama {CROSS_MODEL} @ {OLLAMA_HOST} (cross-provider)")
    try:
        import anthropic  # noqa: F401
    except Exception:
        return (False, "anthropic SDK not installed (pip install anthropic)")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return (False, "ANTHROPIC_API_KEY not set")
    return (True, "anthropic SDK + ANTHROPIC_API_KEY present")


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def _ollama_call(prompt, temperature, num_predict=320):
    payload = {"model": CROSS_MODEL, "prompt": prompt, "stream": False,
               "think": False,  # a thinking model would otherwise burn the budget reasoning
               "options": {"temperature": temperature, "num_predict": num_predict}}
    url = f"{OLLAMA_HOST}/api/generate"
    for body in (payload, {k: v for k, v in payload.items() if k != "think"}):
        try:
            data = json.dumps(body).encode()
            req = urllib.request.Request(url, data=data,
                                         headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.loads(r.read()).get("response", "")
        except Exception:
            continue
    return ""


def call_model(model_id, system, user, temperature=0.0):
    """Return the model's raw text for one (system, user) prompt.

    `model_id` may be a tier label (weak/mid/strong -> TIER_MODELS) or a literal model id.
    On the Ollama backend the tier is ignored: every call uses CROSS_MODEL.
    """
    ok, reason = available()
    if not ok:
        raise ModelClientUnset(reason)
    if _backend() == "ollama":
        # one prompt; Ollama has no separate system role on /api/generate, so prepend it.
        return _ollama_call(system + "\n\n" + user, temperature)
    model = TIER_MODELS.get(model_id, model_id)
    msg = _get_client().messages.create(
        model=model, max_tokens=16, temperature=temperature,
        system=system, messages=[{"role": "user", "content": user}])
    return msg.content[0].text
