# AI Data Readiness Checklist
### Repeatable pre-flight check before any dataset is used in an AI tool, copilot, or agent

**1. Freshness**
- [ ] Confirm last-updated date and expected update cadence
- [ ] Flag if data is older than the business use case tolerates

**2. Completeness**
- [ ] Check for missing values in required fields
- [ ] For semi-structured sources, confirm which fields are core vs. optional

**3. Consistency**
- [ ] For structured sources: confirm schema hasn't silently drifted
- [ ] For semi-structured sources: measure % of records sharing the dominant
      field shape; document that downstream consumers must handle variation
- [ ] For unstructured sources: confirm there's no implicit assumption of
      structure that isn't actually there

**4. Metadata & Documentation**
- [ ] Data dictionary exists and is current
- [ ] Field-level business descriptions exist, not just column names
- [ ] Known limitations are documented, not just discovered by the next person

**5. Ownership & Lineage**
- [ ] System of record is identified
- [ ] Owning team / data steward is named (not "TBD")
- [ ] Upstream and downstream dependencies are mapped

**6. Access & Governance**
- [ ] PII/sensitive content scanned and classified
- [ ] Redaction applied before any AI-facing use, where required
- [ ] Retention policy exists and has governance sign-off (not just a
      recommendation waiting on confirmation)

**Scoring guidance:** score each section 0-10, average for an overall
readiness score. A score below 6 in Metadata/Documentation or
Ownership/Lineage should block AI use until addressed — these are the two
dimensions most likely to cause silent failures downstream, since nothing
breaks loudly when documentation is missing; it just quietly degrades trust
in the AI system's output.
