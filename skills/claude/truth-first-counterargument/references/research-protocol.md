# Research protocol

Use this protocol for externally checkable claims. It prevents source laundering, fake precision, and confirmation-biased rebuttals.

## Contents

1. Frame the research question
2. Construct the query map
3. Follow the source ladder
4. Trace provenance and independence
5. Audit source quality
6. Maintain the evidence ledger
7. Test both sides
8. Calibrate confidence
9. Apply stopping rules

## 1. Frame the research question

Rewrite each atomic claim as a question with explicit boundaries:

- Who or what is being described?
- What exactly happened or is alleged?
- Where and under which jurisdiction?
- During which period?
- Compared with what baseline?
- Which definition, unit, denominator, or population applies?
- What evidence would prove the claim wrong?

Record the user's paraphrase separately from the target's exact words. A rebuttal to a paraphrase can become a straw man.

Treat user-supplied screenshots, summaries, transcripts, and source descriptions as **provided but not independently verified** until the original material or an independent copy is opened. Preserve that label in the evidence ledger.

## 2. Construct the query map

Create three to seven searches covering different failure modes:

1. exact quote or title;
2. original speaker, document, dataset, paper, judgment, or recording;
3. neutral description of the claim;
4. strongest support for the claim;
5. strongest criticism or correction;
6. methodology, denominator, definitions, or raw data;
7. corrections, retractions, later updates, or archived versions.

Search in the source language and the user's language when relevant. Use date filters only when they match the event, not merely the publication cycle.

## 3. Follow the source ladder

Prefer evidence in this order, while still auditing each item:

1. original records: raw data, legislation, court decisions, filings, full recordings, primary texts, official statistics;
2. transparent synthesis: systematic reviews, peer-reviewed research, standards, audit reports, documented expert consensus;
3. independent reporting that links or quotes the original evidence in context;
4. qualified analysis with disclosed method and conflicts;
5. advocacy, opinion, influencer content, anonymous posts, and aggregators as leads—not final proof.

An official source may have incentives or measurement limits. A partisan source may still reproduce valid primary evidence. Judge the method and provenance, not only the label.

## 4. Trace provenance and independence

For every important number, quote, clip, or image, ask:

- Where did this first appear?
- Is the full document or recording available?
- Do later articles cite the same wire story, press release, anonymous source, or study?
- Has the material been cropped, translated, edited, or stripped of qualifying language?
- Is the claimed date the event date, upload date, or republication date?
- Is an old event being presented as current?

Assign an `independence_group` to each evidence item. Articles that repeat one origin belong to the same group. Ten copies of one unsupported statement equal one origin, not ten confirmations.

Watch for circular sourcing:

1. outlet A cites outlet B;
2. outlet B cites a social post;
3. the social post cites outlet A.

Treat that loop as no independent confirmation until an original source is found.

## 5. Audit source quality

Score each dimension separately; do not collapse reputation into one label.

| Dimension | 0 | 1–2 | 3–4 |
|---|---|---|---|
| Source quality | unknown/fabricated | advocacy or weak controls | primary, audited, peer-reviewed, or highly transparent |
| Directness | hearsay | summary or indirect proxy | directly measures/documents the claim |
| Relevance | wrong scope/date | partial match | same scope, period, population, and definition |
| Transparency | no method | incomplete method | data, method, limits, and corrections visible |
| Materiality | peripheral | useful context | changes the core verdict |

Also record:

- author and publisher;
- publication and event dates;
- funding, sponsorship, affiliation, and disclosed conflicts;
- correction or retraction history;
- sample, denominator, measurement method, and uncertainty;
- whether the headline matches the body;
- whether the source distinguishes fact, allegation, and opinion.

Red flags are reasons to investigate, not automatic proof of falsehood.

## 6. Maintain the evidence ledger

Use one row per evidence item:

| ID | Atomic claim | Stance | Exact support | Source | Origin group | Date | Quality | Directness | Limits |
|---|---|---|---|---|---|---|---:|---:|---|

Stance values:

- supports;
- contradicts;
- mixed;
- context only.

Quote minimally. Link to the exact page or section. Record the claim supported by the source, not just the topic it discusses.

## 7. Test both sides

Run two falsification passes:

### Target-claim test

- What is the strongest evidence against the target?
- Does the target survive narrower definitions and correct denominators?
- Is causation being inferred from correlation or sequence?

### User-rebuttal test

- What is the strongest evidence against the user's preferred answer?
- Is the rebuttal relying on one exceptional case against a population claim?
- Does it shift the definition or burden of proof?
- Would a fair opponent accept the stated premise but reject the conclusion?

If the rebuttal fails and the target survives, recommend concession.

## 8. Calibrate confidence

Keep two dimensions separate:

- **truth estimate**: current balance of evidence for the atomic claim;
- **research confidence**: confidence that the search found and correctly interpreted the decisive evidence.

High truth estimate plus low research confidence means “currently looks true, but coverage is weak,” not “proven.”

Limit extremity when:

- only one independent origin exists;
- no direct evidence exists;
- definitions or time periods differ;
- the primary material is inaccessible;
- experts disagree for methodological reasons;
- the user supplied only a cropped clip or paraphrase.

Round to the nearest 5 by default. Explain the decisive reason and what would move the estimate.

## 9. Apply stopping rules

Stop when:

- every load-bearing claim has direct or transparently indirect evidence;
- the original source chain is known or its absence is material and reported;
- at least one serious counter-source was examined;
- remaining disagreement is definitional, normative, or genuinely unresolved;
- additional results repeat existing origin groups.

Continue when a decisive citation is still a snippet, an inaccessible secondary reference, a shared-origin echo, or an unverified translation.
