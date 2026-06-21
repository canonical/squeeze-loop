#!/usr/bin/env python3
"""Cross-provider disjoint judge for the editorial gate (the gold standard Gate A asks for).

The standing editorial gate (verify/editorial_gate.py) is satisfied by a disjoint editorial
review. A SAME-provider-family judge (e.g. a Claude sub-agent reviewing a Claude-authored
paper) is only PARTIAL disjointness: R3 (Section 7) shows same-family casts share the author's
blind spot. The gold standard is a CROSS-PROVIDER model -- independent pretraining, so it does
not share the author's blind spots -- or a human.

This script runs a cross-provider model as a framing-consistency judge and records the result
to claims/cross_provider_review.md. It is honesty-gated and NEVER fakes:

  - Pluggable client. Two backends, tried in order:
      1. OpenAI-compatible HTTP (OPENAI_API_KEY [+ optional OPENAI_BASE_URL, CROSS_MODEL]).
         Use this for a CAPABLE cross-provider judge (GPT/Gemini/etc. via an OpenAI-compatible
         endpoint or OpenRouter). This is the gold standard.
      2. Ollama at OLLAMA_HOST (default http://localhost:11434; may be a remote host, e.g.
         http://localhost:11434) -- a genuinely cross-provider family (e.g. Qwen, Llama,
         Mistral). With CROSS_MODEL set to a capable model (e.g. a 27B Qwen) this is also a
         gold-standard judge; CROSS_MODEL is used as-is even if not in the auto-detect list.
  - No backend reachable => loud SKIP (exit 3). Nothing fabricated.
  - CONTROLS FIRST. Before trusting any verdict, the judge must pass two control probes: a
    known-CONTRADICTION pair and a known-CONSISTENT pair. A model that fails a control is
    recorded as INSUFFICIENT (not authoritative) -- true disjointness does not buy capability.

Output: claims/cross_provider_review.md (an artifact; editorial_gate.py reads it for the
cross-provider status). Non-deterministic -> logged, not gated as a hard pass/fail.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "claims" / "cross_provider_review.md"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")

# Models whose pretraining is independent of the author (claude-opus-4-8, Anthropic).
AUTHOR_PROVIDER = "anthropic"
PROVIDER_OF = {"qwen": "alibaba", "llama": "meta", "mistral": "mistralai",
               "gemma": "google", "phi": "microsoft", "gpt": "openai",
               "deepseek": "deepseek"}


def provider_of(model: str) -> str:
    m = model.lower()
    for k, v in PROVIDER_OF.items():
        if k in m:
            return v
    return "unknown"


def _http(url, payload, timeout=120, headers=None):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers or {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def openai_client():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("CROSS_MODEL", "gpt-4o-mini")

    def call(prompt):
        out = _http(f"{base}/chat/completions",
                    {"model": model, "temperature": 0,
                     "messages": [{"role": "user", "content": prompt}]},
                    headers={"Content-Type": "application/json",
                             "Authorization": f"Bearer {key}"})
        return out["choices"][0]["message"]["content"]
    return ("openai-compatible", model, call)


def ollama_client():
    # Host is OLLAMA_HOST (default localhost); may be a remote LAN/host machine.
    try:
        with urllib.request.urlopen(f"{OLLAMA}/api/tags", timeout=8) as r:
            tags = json.loads(r.read())
    except Exception:
        return None
    names = [m["name"] for m in tags.get("models", [])]
    forced = os.environ.get("CROSS_MODEL")
    if forced:
        # an explicitly named model is used as-is, even if it is not in the
        # auto-detect list (e.g. a remote host's capable cross-provider model).
        model = forced
    else:
        # otherwise pick a non-embedding generative model with an independent provider
        cand = [n for n in names if "embed" not in n.lower() and provider_of(n) != "unknown"]
        if not cand:
            return None
        model = cand[0]

    def call(prompt):
        try:
            out = _http(f"{OLLAMA}/api/generate",
                        {"model": model, "prompt": prompt, "stream": False,
                         "think": False,  # a thinking model would otherwise spend the budget reasoning
                         "options": {"temperature": 0, "num_predict": 512}})
        except Exception:
            # retry without the think toggle for Ollama versions that reject it
            try:
                out = _http(f"{OLLAMA}/api/generate",
                            {"model": model, "prompt": prompt, "stream": False,
                             "options": {"temperature": 0, "num_predict": 512}})
            except Exception:
                return ""
        return out.get("response", "")
    return ("ollama", model, call)


def verdict_token(text):
    up = (text or "").upper()
    # take the first of the two tokens that appears
    ci, ki = up.find("CONTRADICT"), up.find("CONSISTENT")
    if ci < 0 and ki < 0:
        return "?"
    if ci < 0:
        return "CONSISTENT"
    if ki < 0:
        return "CONTRADICT"
    return "CONTRADICT" if ci < ki else "CONSISTENT"


def probe(call, a, b):
    p = (f"Two sentences from a paper.\nA: \"{a}\"\nB: \"{b}\"\n"
         "Do A and B contradict each other? Answer exactly CONTRADICT or CONSISTENT, "
         "then one short reason.\nAnswer:")
    raw = call(p)
    return verdict_token(raw), (raw or "").strip().replace("\n", " ")[:160]


CONTROLS = [
    ("contradiction", "CONTRADICT",
     "in-house evidence comes in two coordinate strands, neither ranked above the other.",
     "the reflexive case study is the single strongest in-house evidence."),
    ("consistency", "CONSISTENT",
     "the comparison is exploratory and small-n.",
     "a powered, multi-tier comparison remains future work."),
]
# Live probe: the current paper's actual Section 5 (real-world / lace) framing. Should be
# CONSISTENT -- the strong-sounding "found real defects" finding is deliberately bounded as a
# case study, not an efficacy claim; a CONTRADICT verdict would mean that hedge had broken.
LIVE = ("applied to an external UEFI bootloader, the strategy found four real security defects in production code.",
        "the lace application is a case study, not a controlled efficacy comparison, and not a full verification of that codebase.")


def main():
    client = openai_client() or ollama_client()
    if not client:
        print("=== Cross-provider review: SKIPPED ===")
        print("  No cross-provider backend reachable.")
        print("  Set OPENAI_API_KEY (+CROSS_MODEL), or OLLAMA_HOST + CROSS_MODEL pointing at a")
        print("  reachable Ollama with a capable cross-provider model, for the gold-standard judge.")
        print("  Nothing fabricated.")
        return 3

    backend, model, call = client
    prov = provider_of(model)
    disjoint = prov != AUTHOR_PROVIDER and prov != "unknown"
    print(f"=== Cross-provider disjoint review ({backend}: {model}, provider={prov}) ===")
    print(f"  author provider = {AUTHOR_PROVIDER}; judge provider = {prov} -> "
          f"{'CROSS-PROVIDER (independent pretraining)' if disjoint else 'NOT cross-provider'}")

    # controls first
    ctrl_ok = True
    ctrl_lines = []
    for name, expect, a, b in CONTROLS:
        got, reason = probe(call, a, b)
        ok = got == expect
        ctrl_ok = ctrl_ok and ok
        ctrl_lines.append(f"  control[{name}]: expected {expect}, got {got} -> {'OK' if ok else 'FAIL'}  ({reason})")
        print(ctrl_lines[-1])

    got, reason = probe(call, *LIVE)
    print(f"  live framing probe: {got}  ({reason})")

    authoritative = disjoint and ctrl_ok
    status = ("AUTHORITATIVE (cross-provider and passes controls)" if authoritative
              else "NON-AUTHORITATIVE: " + ("not cross-provider" if not disjoint
                    else "fails a control probe -> insufficient capability"))
    print(f"\n  cross-provider status: {status}")

    OUT.write_text(
        f"# Cross-provider disjoint review (editorial gate, gold-standard axis)\n\n"
        f"backend: {backend}\nmodel: {model}\njudge-provider: {prov}\n"
        f"author-provider: {AUTHOR_PROVIDER}\n"
        f"cross-provider: {'yes (independent pretraining)' if disjoint else 'no'}\n"
        f"controls-passed: {ctrl_ok}\n"
        f"authoritative: {authoritative}\n"
        f"status: {status}\n\n"
        "## probes\n" + "\n".join(ctrl_lines) +
        f"\n  live framing probe: {got}  ({reason})\n\n"
        "Non-deterministic (model output); logged, not gated. The standing editorial verdict "
        "in editorial_review.md remains the operative one; this records the cross-provider axis "
        "(R3: provider-disjointness vs capability). A capable cross-provider judge "
        "(OPENAI_API_KEY + CROSS_MODEL, or OLLAMA_HOST + CROSS_MODEL) is the gold standard; it "
        "corroborates the framing but is a narrow framing-consistency probe, not the full "
        "editorial review.\n")
    print(f"  recorded -> {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
