# Output contract

Use the user's language. Keep the visible structure compact enough for the requested medium while preserving evidence and uncertainty.

## Priority overrides

These rules override every template below:

1. If the concede route wins and no material overreach remains, answer in two to four sentences and stop.
2. Give a percentage only when an adequate, source-audited evidence ledger exists. Otherwise write `Truth estimate: Not scored — live verification unavailable` / `Doğruluk tahmini: Puanlanmadı — canlı doğrulama yok`.
3. Omit empty sections. Do not show “Sources” without sources or “Likely comeback” without a material comeback.
4. Default to roughly 60 words for a simple concession and 150 words for a quick reply unless the user asks for detail.
5. For hypothetical or fictional inputs, put a visible simulation label above any verdict or score.

## Contents

1. Full-analysis layout
2. Quick-reply layout
3. Case-file update layout
4. Verdict and confidence language
5. Citation rules
6. Response variants

## 1. Full-analysis layout

Use this default structure.

### Verdict / Hüküm

Lead with four fields:

- **Core claim / Çekirdek iddia:** one neutral sentence;
- **Truth estimate / Doğruluk tahmini:** percentage, normally rounded to 5, or “not scored” when evidence access is inadequate;
- **Research confidence / Araştırma güveni:** low, medium, or high;
- **Decision / Karar:** concede, narrow, clarify, counter values, or rebut.

Add a one-sentence reason. If the target is mostly right, say so here rather than hiding it below.

### Claim audit / İddia denetimi

| Atomic claim / Alt iddia | Estimate / Tahmin | Verdict / Sonuç | Decisive evidence or gap / Belirleyici kanıt veya boşluk |
|---|---:|---|---|

Keep one row per testable claim. For normative claims, write “value judgment / değer yargısı” instead of a fake truth percentage and score the factual premises separately.

### Strongest honest response / En güçlü dürüst cevap

Provide one ready-to-use response in natural language. It must:

- concede supported points;
- focus on one load-bearing weakness;
- avoid claims not supported by the ledger;
- sound like a person, not a debate textbook;
- remain defensible if quoted without surrounding context.

### Why it works / Neden işe yarıyor

Explain the logic in two to five short points:

1. premise accepted;
2. premise disputed;
3. decisive evidence;
4. inference to the conclusion;
5. remaining value disagreement, if any.

### Likely comeback / Muhtemel dönüş (when material)

Give the strongest informed comeback and the best evidence-consistent answer only when it stress-tests a material weakness or the user asks for debate preparation. If the comeback exposes a real weakness, revise the main response instead of pretending to defeat it.

### Do not say / Şunu söyleme

Name one or two tempting overclaims, weak statistics, fallacy labels, or personal attacks that would make the user's position easier to rebut.

### Sources / Kaynaklar

List only sources actually used. For each source, state what it supports. Put claim-level links near the relevant sentence as well.

### Uncertainty / Belirsizlik

State:

- what remains unknown;
- what evidence would change the verdict;
- the last verified date for changing claims.

## 2. Quick-reply layout

Use when the user asks “Ne diyeyim?” or needs a social-media reply.

```markdown
## Kısa hüküm
**Tahmin:** 70% doğru _veya_ Puanlanmadı — canlı doğrulama yok · **Güven:** Orta · **Karar:** Tam karşı çıkma; iddiayı daralt

## Yazabileceğin cevap
> ...

## Dayanak
- ... [source]
- ... [source]

## Muhtemel dönüş → cevabın
**Dönüş:** ...
**Cevap:** ...

## Söyleme
- ...
```

English labels:

```markdown
## Quick verdict
**Estimate:** 70% true _or_ Not scored — live verification unavailable · **Confidence:** Medium · **Decision:** Narrow, do not fully oppose

## Ready-to-use reply
> ...

## Evidence
- ... [source]

## Likely comeback → answer
...

## Do not claim
- ...
```

## 3. Case-file update layout

For follow-up turns, avoid repeating the whole report.

```markdown
## Vaka güncellemesi
**Yeni kanıt:** ...
**Etkilenen alt iddia:** C2
**Eski → yeni tahmin:** 55% → 75%
**Neden değişti:** ...
**Güncel en güçlü cevap:** ...
**Hâlâ belirsiz:** ...
```

Preserve source IDs and independence groups across turns. Update the “last verified” date.

## 4. Verdict and confidence language

Do not write “the truth rate is exactly 73.4%” unless a real model produces that statistical probability. Prefer:

> “Available evidence supports this at roughly 70%; research confidence is medium because the decisive data comes from two independent but partly indirect sources.”

Turkish:

> “Mevcut kanıtlar bu iddiayı yaklaşık %70 destekliyor; belirleyici veriler iki bağımsız fakat kısmen dolaylı kaynaktan geldiği için araştırma güveni orta.”

Use “unresolved” when evidence is incomparable, not “50% true” as a rhetorical shortcut. Use “not scored” rather than a number when live evidence was not retrieved or the ledger is only hypothetical.

## 5. Citation rules

- Cite the exact primary page, dataset, full recording, paper, judgment, or correction when available.
- Place the citation next to the claim it supports.
- Do not cite search result pages or snippets.
- Do not use one source to support a broader statement than it actually covers.
- Mark archived copies and explain why the live page is unavailable.
- Distinguish quotation, paraphrase, calculation, and inference.
- Name a shared upstream origin when several outlets repeat it.
- Respect quotation and copyright limits; summarize rather than copying long passages.

## 6. Response variants

Do not flood the user with variants. Default to one calm version. Add at most two alternatives when useful:

- **Everyday / Halk ağzı:** shorter and natural;
- **Firm / Net:** direct but respectful;
- **Question-led / Soru odaklı:** exposes the decisive missing premise.

Every variant must preserve the same verified factual core. Tone may change; truth must not.
