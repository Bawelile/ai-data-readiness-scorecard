"""
AI Data Readiness Scorecard
Scores a dataset's readiness for AI/copilot/agent consumption across the
dimensions named explicitly in the target JD: quality, freshness, metadata,
access/governance, ownership, and lineage. Applied here to the three
Meridian Retail Group sources built in Project 1 — this project answers
"is this data ready for an AI system to use?", not "what does the data say?"
"""
import json
import csv
import os
from datetime import date, datetime
from collections import Counter

BASE_M = "/home/claude/meridian"      # Project 1 outputs (reused, not rebuilt)
BASE = "/home/claude/ai-readiness"

TODAY = date(2026, 1, 1)  # one day after the synthetic data's last date

# ---------------------------------------------------------------------------
# Scoring dimensions — named to match the JD directly:
#   "quality, freshness, metadata, and access expectations"
#   "accuracy, completeness, consistency, and timeliness"
#   "metadata, documentation, and business descriptions"
#   "classification, access controls, and retention"
#   "data lineage and ownership documentation"
# ---------------------------------------------------------------------------

def score_sql_source():
    with open(f"{BASE_M}/sql/transactions.csv") as f:
        rows = list(csv.DictReader(f))
    dates = [datetime.fromisoformat(r["txn_date"]).date() for r in rows]
    max_date = max(dates)
    freshness_days = (TODAY - max_date).days
    freshness_score = 10 if freshness_days <= 1 else max(0, 10 - freshness_days)

    required_fields = ["txn_id","txn_date","store_id","sku","product_name",
                        "category","unit_price","unit_cost","units_sold","promo_flag"]
    missing = sum(1 for r in rows for f in required_fields if not r.get(f))
    completeness_score = round(10 * (1 - missing / (len(rows) * len(required_fields))), 1)

    # Consistency: single fixed schema across all rows (CSV guarantees this),
    # but we still check for outlier values (negative prices/units) as a
    # quality-consistency check, not just a schema check.
    bad_values = sum(1 for r in rows if float(r["unit_price"]) <= 0 or int(r["units_sold"]) < 0)
    consistency_score = round(10 * (1 - bad_values / len(rows)), 1) if rows else 0

    # Metadata & documentation: does a data dictionary exist yet? (it doesn't,
    # until the remediation step below creates one)
    metadata_score = 2  # column names are self-explanatory but no formal dictionary/units doc exists

    # Ownership & lineage: no documented owner/source-system record exists yet
    ownership_score = 2

    # Access/governance classification: transactional data, no PII, low sensitivity
    access_score = 9

    return {
        "source": "SQL — transactions.csv",
        "row_count": len(rows),
        "freshness": freshness_score,
        "completeness": completeness_score,
        "consistency": consistency_score,
        "metadata_documentation": metadata_score,
        "ownership_lineage": ownership_score,
        "access_governance": access_score,
    }


def score_nosql_source():
    with open(f"{BASE_M}/nosql/support_tickets.json") as f:
        tickets = json.load(f)
    dates = [datetime.fromisoformat(t["date"]).date() for t in tickets]
    max_date = max(dates)
    freshness_days = (TODAY - max_date).days
    freshness_score = 10 if freshness_days <= 1 else max(0, 10 - freshness_days)

    core_fields = ["ticket_id","customer_name","email","channel","date","sku","complaint_type","tags"]
    missing = sum(1 for t in tickets for f in core_fields if f not in t or not t[f])
    completeness_score = round(10 * (1 - missing / (len(tickets) * len(core_fields))), 1)

    # Consistency: measure schema drift — % of docs that share the exact
    # same key set as the most common key set. Intentionally inconsistent
    # by design (some docs have refund_amount/sentiment_score/resolution,
    # some don't) — this is the honest, realistic NoSQL finding.
    key_sets = [tuple(sorted(t.keys())) for t in tickets]
    most_common_shape, count = Counter(key_sets).most_common(1)[0]
    consistency_score = round(10 * (count / len(tickets)), 1)

    metadata_score = 3  # tags field gives some semantic structure; no formal schema doc
    ownership_score = 2  # no documented owning team (support platform vendor unclear)
    access_score = 6     # contains customer email/name directly in structured fields — Internal sensitivity

    return {
        "source": "NoSQL — support_tickets.json",
        "row_count": len(tickets),
        "freshness": freshness_score,
        "completeness": completeness_score,
        "consistency": consistency_score,
        "metadata_documentation": metadata_score,
        "ownership_lineage": ownership_score,
        "access_governance": access_score,
        "schema_consistency_note": f"Only {count}/{len(tickets)} documents ({round(100*count/len(tickets),1)}%) share the exact same field set — expected and realistic for a NoSQL source, but it means downstream consumers (including an AI system) must handle missing fields gracefully rather than assume a fixed shape."
    }


def score_unstructured_source():
    with open(f"{BASE_M}/output/pii_classification_report.json") as f:
        pii_report = json.load(f)
    n = len(pii_report)
    restricted = sum(1 for r in pii_report if r["sensitivity"] == "Restricted")
    internal = sum(1 for r in pii_report if r["sensitivity"] == "Internal")

    freshness_score = 10  # same batch as the other sources, same date range
    completeness_score = 8  # free text is inherently "complete" as-is, minor deduction for no structured fields
    consistency_score = 3  # unstructured text has no consistent structure at all — honest low score

    # This is the one dimension that's ALREADY strong, because Project 1
    # built the redaction/classification layer — reusing it here rather
    # than rebuilding it.
    access_score = 9  # every file scanned, classified, and redacted before any downstream use
    metadata_score = 1  # raw text files have no metadata beyond a filename
    ownership_score = 2  # no documented source-system owner for the raw complaint intake channel

    return {
        "source": "Unstructured — complaint text files (post Project 1 PII layer)",
        "row_count": n,
        "freshness": freshness_score,
        "completeness": completeness_score,
        "consistency": consistency_score,
        "metadata_documentation": metadata_score,
        "ownership_lineage": ownership_score,
        "access_governance": access_score,
        "governance_note": f"{restricted} Restricted + {internal} Internal files were classified and redacted in Project 1 before any use — this dimension is strong specifically BECAUSE that governance layer already exists, which is the point: readiness work compounds across projects instead of restarting each time."
    }


def overall_score(s):
    dims = ["freshness","completeness","consistency","metadata_documentation","ownership_lineage","access_governance"]
    return round(sum(s[d] for d in dims) / len(dims), 1)


sources = [score_sql_source(), score_nosql_source(), score_unstructured_source()]
for s in sources:
    s["overall_readiness_score"] = overall_score(s)

os.makedirs(BASE + "/output", exist_ok=True)
with open(f"{BASE}/output/readiness_scorecard_before.json", "w") as f:
    json.dump(sources, f, indent=2)

print("=== AI Data Readiness Scorecard — BEFORE remediation ===\n")
for s in sources:
    print(f"{s['source']}")
    print(f"  Overall readiness: {s['overall_readiness_score']}/10")
    print(f"  Freshness={s['freshness']}  Completeness={s['completeness']}  "
          f"Consistency={s['consistency']}  Metadata/Docs={s['metadata_documentation']}  "
          f"Ownership/Lineage={s['ownership_lineage']}  Access/Governance={s['access_governance']}\n")
