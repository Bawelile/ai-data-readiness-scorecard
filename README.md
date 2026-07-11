# AI Data Readiness Scorecard
### Is this data actually ready for an AI system to use — or does it just look ready?

*Built specifically against the requirements of a real AI Data Analyst job
posting focused on data readiness, quality, metadata, and governance for
AI-consumed data. Reuses the multi-source pipeline and PII/governance layer
from [Project 1](../Multi-Source-Pricing-Intelligence-Platform) rather than rebuilding
from scratch — readiness work should compound, not restart.*

## The problem

Before any dataset gets used by an AI tool, copilot, or agent, someone has
to answer a less exciting question than "what does the model say" —
**is this data actually trustworthy enough to hand to an AI system in the
first place?** Stale data, unclear ownership, missing metadata, and
undocumented sensitivity all produce the same failure mode: an AI system
that looks confident while quietly working from bad inputs.

## What I built

A scoring engine that evaluates any dataset across six dimensions, all
pulled directly from language used in real AI-readiness job postings:
**freshness, completeness, consistency, metadata & documentation,
ownership & lineage, and access/governance classification.**

Applied to the three Project 1 sources:

| Source | Before | After remediation |
|---|---|---|
| SQL — transactions | 7.2 / 10 | **9.3 / 10** |
| NoSQL — support tickets | 5.6 / 10 | **7.6 / 10** |
| Unstructured — complaint text | 5.5 / 10 | **6.7 / 10** |

The "after" scores aren't a re-rating — they reflect real artifacts
generated as remediation: a data dictionary for the SQL source, an
ownership/lineage record across all three sources, and a repeatable AI
Data Readiness Checklist any team could reuse on a new dataset.

## What I deliberately did NOT fix

Two sources still show an open "data steward: TBD" flag after
remediation. That's intentional. A checklist can document that ownership
is unclear — it can't manufacture a real person or team accepting
responsibility. Scoring those dimensions a false 10/10 would have made the
tool look more complete than it actually is, which defeats the purpose of
a readiness check in the first place. The honest partial credit (4/10, not
0 and not 10) is the actual finding.

## Why this reuses Project 1 instead of starting over

The unstructured source's Access/Governance score is strong (9/10)
specifically *because* Project 1's PII detection and redaction layer
already exists — this project didn't rebuild that work, it built on top
of it. That's the same "readiness compounds" principle the scorecard is
meant to encourage in a real data organization, applied to how I structured
my own project sequence.

## Deliverables

- `scripts/01_scorecard_before.py` — scoring engine, run against real
  computed metrics (not hardcoded scores) from Project 1's actual files
- `scripts/02_remediation.py` — generates the missing governance artifacts
  and re-scores
- `output/governance_docs/sql_data_dictionary.json` — field-level data
  dictionary
- `output/governance_docs/ownership_lineage_record.json` — system of
  record, owning team, upstream/downstream mapping for all three sources
- `output/governance_docs/AI_READINESS_CHECKLIST.md` — the repeatable
  checklist deliverable, reusable on any new dataset
- `output/dashboard.html` — standalone before/after dashboard with an
  explicit open-action-items table

## Tech stack

`Python` `Data quality scoring` `Metadata & lineage documentation` `Data governance frameworks` `JSON schema analysis`

---

*Part of a broader portfolio demonstrating end-to-end analytical and data
governance work. See [Bawelile.github.io](https://Bawelile.github.io) for
the full project set, including Project 1, which this project builds on.*
d
