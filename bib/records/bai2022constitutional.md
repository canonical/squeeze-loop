bibkey: bai2022constitutional
citation: Yuntao Bai, Saurav Kadavath, Sandipan Kundu, et al. (Anthropic). "Constitutional AI: Harmlessness from AI Feedback." arXiv:2212.08073, 2022.
arxiv: 2212.08073   read: FULL (via ar5iv/arxiv-html)   access-date: 2026-06-12

CLAIM CARDS

1. Quote (§3.1): "we first generate responses to harmfulness prompts using a helpful-only AI assistant. These initial responses will typically be quite harmful and toxic. We then ask the model to critique its response according to a principle in the constitution."
   Anchor: §3.1 "Method" (Supervised Stage critique-revision).
   Paraphrase: In the SL stage, a single helpful model generates a (harmful) response and is then prompted, in-context, to critique that response against a sampled constitutional principle.

2. Quote (§3.1, prompt example): "Critique Request: Identify specific ways in which the assistant's last response is harmful, unethical, racist, sexist, toxic, dangerous, or illegal."
   Anchor: §3.1 example critique-revision template.
   Paraphrase: The critique is driven by an explicit normative instruction; the model then revises its own prior turn based on its critique.

3. Quote (§4, RL stage): RLAIF uses "AI Feedback" - the model evaluates response pairs against constitutional principles formatted as multiple-choice questions, producing labels for a preference model that then drives RL.
   Anchor: §4 "Constitutional AI: Reinforcement Learning from AI Feedback".
   Paraphrase: Phase 2 is distinct: a feedback model labels comparisons by the constitution, a preference model is trained, and the policy is RL-optimized against it (no human harm labels).

METHOD: Constitutional AI trains a harmless assistant in two phases. Phase 1 (supervised): a helpful model self-critiques and revises its harmful answers against sampled constitution principles, and is finetuned on the revisions. Phase 2 (RLAIF): the finetuned model generates response pairs, an AI feedback model picks the more harmless option using the constitution, and a preference model trained on those AI labels guides RL.

LIMITATIONS (authors' own): The constitution is short and hand-written, so principle selection and wording strongly shape behavior; relying on AI feedback can amplify model biases and reduce human oversight; there are tensions between helpfulness and harmlessness and risk of over-refusal / evasiveness.

CONTRIBUTION: Cited for "Constitutional AI critiques generations against an explicit normative document ... though in its self-critique stage generator and critic share weights and context." Body confirms (a) the explicit normative document = the constitution, (b) the two-phase SL-critique-revision vs RLAIF structure, and (c) that in the SL self-critique stage the SAME helpful model both generates and critiques in-context (shared weights and context). VERDICT: SUPPORTED. The "self-critique stage" qualifier is accurate: shared-weights/shared-context applies specifically to the Phase-1 critique-revision step, not to Phase-2 RLAIF (which uses a separately-prompted feedback model and a trained preference model). Qualifier correctly scopes the claim.
