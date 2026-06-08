# CLAUDE.md — working rules for this repo

A synthesis framework about learning (cognitive science + educational psychology).
The literature was gathered with heavy AI assistance, so the highest risk is
AI-introduced errors at the citation/evidence layer. These rules exist to contain
that risk. This file is rules to act on, not documentation — keep it lean;
documentation lives in README.

## Before every commit
- Run `python checks/integrity.py` and fix any failure. It verifies bibliography
  contiguity, that every in-text `[n]` resolves, and that claim titles are
  character-identical between framework and compendium (the join key). Never
  commit on a red check.

## Citations — verify before entry (the rule violated most often)
- No citation enters or changes unless you have confirmed, against the actual
  source, that (a) the work exists with the cited authors/venue/year and (b) it
  actually supports the claim it is attached to. Not from memory, not from a
  snippet. A citation that "sounds right" has been wrong here repeatedly.
- When removing a claim, check whether a reference was cited only by it before
  removing the reference. Prefer a documented `*(intentional gap; …)*` marker
  over renumbering the bibliography.

## Claims
- Check population/age-band fit, not just topical fit. The framework targets a
  normally-developing learner; clinical, adult, or atypical-population evidence
  does not transfer to it. If a verification question needs the prefix "the
  struggling/dysregulated learner," that framing is already selecting the wrong
  population.
- Don't make a contested mechanism load-bearing. Assert the well-supported
  descriptive core; leave the disputed mechanism out.
- Claim titles are the join key: change a title in both files and re-run the check.

## Where things live (don't cross these)
- Claim bodies hold only the claim's own content. Rationale, provenance, and
  "why added/dropped" belong in separate working notes — never in a claim body.
  Do not narrate deliberation inside a claim (e.g. "this differs from T7 because…").
- Stable beliefs go in the framework and compendium; transient working state does not.
- Distinguish meta-conversation (how to work) from document content. Process and
  workflow instructions are not framework material; when it is ambiguous whether
  something belongs in a document, ask before writing it in.

The maintainer keeps private working files (provenance notes, an audit docket,
handoff notes) that are not in this repo, plus a gitignored `CLAUDE.local.md`.
If you are in the maintainer's local checkout, follow `CLAUDE.local.md` — it
covers those files and personal working style. Their absence does not affect the
rules above.
