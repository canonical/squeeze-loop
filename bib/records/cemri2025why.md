bibkey: cemri2025why
citation: Cemri, M., Pan, M. Z., Yang, S., Agrawal, L. A., Chopra, B., Tiwari, R., Keutzer, K., Parameswaran, A., Klein, D., Ramchandran, K., Zaharia, M., Gonzalez, J. E., & Stoica, I. (2025). Why Do Multi-Agent LLM Systems Fail? arXiv:2503.13657.
arxiv: 2503.13657   read: ABSTRACT (arXiv abstract page)   access-date: 2026-06-15

CLAIM CARDS

1. Quote: "system design issues, (ii) inter-agent misalignment, and (iii) task verification" (abstract) -> Paraphrase: The taxonomy groups multi-agent failures into three categories, two of which are inter-agent misalignment and (weak) task verification.

2. Quote: "14 unique modes" (abstract) -> Paraphrase: Fourteen distinct failure modes are catalogued across the three categories, from an empirical trace study.

METHOD
MAST (Multi-Agent System failure Taxonomy) built from 1,600+ annotated traces across 7 frameworks; 150 traces expert-annotated with high inter-annotator agreement (kappa = 0.88).

LIMITATIONS (authors' own)
Taxonomy derived from a finite set of frameworks/traces; the authors note the identified failures require more sophisticated solutions (a research roadmap, not a fix).

CONTRIBUTION (why cited here)
Supports the manuscript's claim that a recent multi-agent-LLM failure taxonomy finds weak verification and inter-agent misalignment among the most common breakdowns -- the empirical backdrop the squeeze is built against. VERDICT: SUPPORTED (categories (ii) and (iii) name exactly these). Used as motivation, not as a quantitative result.
