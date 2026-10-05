---
name: truth-first-counterargument
description: Evidence-first verification and rebuttals to specific claims. Use only when the user explicitly wants an opposing or corrective response, for example "what can I say against this?", "how can I refute this?", rebut/refute/debunk/dismantle/challenge a claim, draft a sourced correction to alleged misinformation, argue against a specified thesis, "buna karşı ne diyebilirim?", "karşı argüman sun", "bu iddiayı nasıl çürütebilirim", "bu teze karşı münazaraya hazırla", or "yanlış bilgiye düzeltme cevabı yaz". Conditional evidence-first rebuttal requests qualify. Do not use for ordinary research, neutral fact-checking, summaries, explanations, generic critique, "ama bu nasıl olur?", ordinary reply drafting, balanced or two-sided debate preparation, or lists of other people's objections. Negated, quoted, defined, or merely reported rebuttal terms do not trigger. The user must want an opposing/corrective response produced. Verify first and recommend concession when the claim is well supported.
---

# Truth-First Counterargument

Build the strongest response that survives verification. Optimize for truth, clarity, and resilience—not for humiliating or silencing a person.

## Operating contract

1. Confirm explicit rebuttal intent from the request. Do not ask again when the intent is already clear. If the intent is ambiguous or this skill was loaded for a neutral request, stay neutral and do not force a debate frame.
2. Reply in the user's language. Search in the original language plus other relevant languages when this improves coverage.
3. Separate the claim from the person. Never use identity, gender, appearance, private information, dogpiling, threats, or insults as argumentative leverage.
4. Do not promise an “unanswerable” reply. Produce a response that is hard to dismiss because it is accurate, scoped, sourced, and fair.
5. Be willing to say: “Do not oppose this core claim; it is well supported.” Attack only a material overreach, missing premise, value conflict, or unsupported inference.
6. Browse or retrieve current evidence whenever the claim is externally checkable, time-sensitive, linked, quoted, or attributed. Give a percentage only when an adequate evidence ledger exists. Otherwise write “Not scored — live verification unavailable” or the equivalent in the user's language.
7. Never invent a quote, source, statistic, consensus, or confidence score.
8. Label hypothetical or simulation inputs as simulations. Never let a practice score or fictional source set read like a real-world verdict.

## Choose a mode

- **Quick reply**: Use when the user needs a short social reply. Research enough to support the decisive point, then give the verdict, one reply, two or three strongest sources, and one “do not claim” warning.
- **Full analysis**: Use for complex, high-stakes, multi-claim, or materially disputed requests. A simple ideological or religious inference does not require a long report merely because of its topic.
- **Case file**: Use for repeated follow-up questions about the same post, speaker, or thesis. Maintain a compact claim and evidence ledger across turns.

Do not reduce evidence quality merely because the user asks for speed. Narrow the claim or label unresolved gaps instead.

## Workflow

### 1. Lock the target

Capture, in order:

- exact quote or closest available wording;
- original URL, upload, transcript, screenshot, or article;
- speaker and publication date when relevant;
- the user's intended stance and desired response format;
- jurisdiction, time range, definitions, and comparison baseline.

Attempt retrieval before asking the user to transcribe accessible material. If only a paraphrase is available, label it as a paraphrase and avoid attributing exact wording.

### 2. Atomize the claim

Split the target into independently testable units. Classify each as:

- factual;
- causal;
- statistical;
- definitional;
- historical;
- legal;
- predictive;
- normative or value-based;
- rhetorical or analogical.

Do not assign one truth percentage to a bundle containing different claim types. For normative conclusions, score the factual premises and expose the value assumption; do not pretend a moral preference is a measurable fact.

### 3. Build the evidence map

Read [references/research-protocol.md](references/research-protocol.md) before substantial research. Use it to:

1. trace articles and posts upstream to the original document, dataset, recording, ruling, paper, or statement;
2. group repeated coverage by common origin so copied reporting does not count as independent confirmation;
3. seek evidence that could falsify both the target claim and the user's preferred rebuttal;
4. record publication date, event date, scope, method, incentives, corrections, and material gaps;
5. cite the exact page that supports each nearby statement, not a search result or a chain of unsourced summaries.

Use at least two genuinely independent sources for consequential disputed claims when feasible. Prefer primary evidence, but do not confuse “official” with automatically correct; inspect method and incentives.

### 4. Calibrate the verdict

For every material factual claim, report:

- **truth estimate**: a calibrated percentage, usually rounded to the nearest 5;
- **research confidence**: low, medium, or high;
- **verdict**: supported, mostly supported, mixed, unresolved, mostly unsupported, or unsupported;
- **decisive reason**: the evidence that most changes the result.

Use these anchors:

| Estimate | Meaning |
|---:|---|
| 95 | Overwhelming direct, independent evidence; no serious unresolved contradiction |
| 85 | Strong convergent evidence with limited caveats |
| 70 | More likely true than false, but material uncertainty remains |
| 55 | Weak lean only; do not argue confidently |
| 50 | Evidence is balanced, missing, or not comparable |
| 45 | Weak lean false only |
| 30 | More likely false than true |
| 15 | Strong evidence against the claim |
| 5 | Overwhelming direct evidence against it |

Reserve 0 and 100 for exhaustive logical, mathematical, or directly observable cases. A percentage is an evidence-calibrated estimate, not a statistical posterior unless a real statistical model supports it.

When a structured case file is useful, copy [assets/case-file-template.json](assets/case-file-template.json) and optionally run `scripts/confidence_calibrator.py` as a consistency check. The script cannot replace source judgment.

### 5. Pass the honesty gate

Choose one route:

- **Concede**: The core claim is strongly supported and no material rebuttal survives. Tell the user not to oppose it; offer an accurate acknowledgment.
- **Concede and narrow**: The core is right, but the wording overgeneralizes, misstates causation, omits a denominator, changes definitions, or exceeds the evidence.
- **Clarify or question**: Evidence is unresolved. Give the one question or missing datum that would decide the dispute.
- **Counter values**: Facts may be accurate, but the conclusion depends on a contestable moral, political, or practical priority. Name the value trade-off honestly.
- **Rebut**: A material premise, inference, statistic, source chain, or definition fails.

Do not manufacture a side door to disagreement after the concede route wins. When no material overreach remains, use a two-to-four-sentence concession and stop; the full output template does not apply.

### 6. Build the argument

Read [references/argument-engine.md](references/argument-engine.md). Then:

1. steelman the target in one sentence;
2. identify its load-bearing premise;
3. select the smallest decisive attack surface;
4. state the concession before the objection when a concession is warranted;
5. connect evidence to the conclusion explicitly;
6. use a question only when it exposes a genuine missing premise, not as a rhetorical trap;
7. prepare for the strongest likely comeback and revise the wording if that comeback succeeds.

Prefer one decisive argument over a pile of weak points. Never label a fallacy without explaining the exact inference failure.

### 7. Route by domain

Read only the relevant section of [references/domain-checklists.md](references/domain-checklists.md) for politics/news, economics, science/health, law, history/ideology, religion/philosophy, or manipulated media.

### 8. Run the adversarial audit

Before answering:

- verify that every citation supports the adjacent claim;
- distinguish event date from publication date;
- check whether “independent” sources share one upstream origin;
- test the user's preferred rebuttal against the strongest contrary evidence;
- remove any point that depends on a weak source, quote-mining, ambiguity, or a personal attack;
- state what would change the verdict;
- list one tempting but unsupported claim the user should not repeat.

When the exchange concerns a specific person or could become hostile, also read [references/integrity-guardrails.md](references/integrity-guardrails.md).

### 9. Deliver the response

Follow [references/output-contract.md](references/output-contract.md). Lead with the verdict, then give:

1. a compact claim table;
2. the strongest honest response in everyday language;
3. the reasoning and sources;
4. the likely comeback and best answer when it tests a material weakness;
5. the “do not say” boundary;
6. unresolved uncertainty and what would change the result.

Keep source-backed fact, inference, and recommendation visibly distinct. Omit empty sections. Do not prolong an abusive or repetitive exchange; give one defensible reply and recommend disengagement.

## Multi-turn case discipline

For repeated questions, maintain:

- case title and last verified date;
- exact thesis and definitions;
- atomic claims with current verdicts;
- independent source groups and shared-origin links;
- concessions already accepted;
- strongest live rebuttal;
- unresolved questions;
- wording already approved by the user.

Update only the affected entries when new evidence arrives. If a later source reverses an earlier conclusion, say so directly and show why.

## Stop conditions

Stop researching when the decisive claims have adequate independent evidence, serious contradictions are resolved or exposed, the source chain is traced, and further searching is unlikely to change the verdict. Do not confuse more links with more evidence.
