# Threat Model: [Product/Feature Name]

**Date:** YYYY-MM-DD
**Author:** Security-Expert
**Status:** Draft | Review | Approved
**Scope:** [What system/feature/boundary this model covers]

---

## Asset Inventory

What are we protecting?

| Asset | Type | Sensitivity | Owner |
|-------|------|-------------|-------|
| | Data / Service / Infrastructure | Low / Medium / High / Critical | |

---

## Trust Boundaries

Where do trust levels change?

| Boundary | From | To | Controls |
|----------|------|----|----------|
| | [lower trust zone] | [higher trust zone] | [auth, validation, encryption, etc.] |

Diagram (optional): Describe or sketch the system boundary map.

---

## Threat Enumeration (STRIDE)

### Spoofing (identity)
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| S1 | | | | Low/Med/High | Low/Med/High/Critical |

### Tampering (data integrity)
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| T1 | | | | | |

### Repudiation (deniability)
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| R1 | | | | | |

### Information Disclosure
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| I1 | | | | | |

### Denial of Service
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| D1 | | | | | |

### Elevation of Privilege
| # | Threat | Affected Asset | Boundary | Likelihood | Severity |
|---|--------|---------------|----------|------------|----------|
| E1 | | | | | |

---

## Risk Matrix

|              | Low Likelihood | Medium Likelihood | High Likelihood |
|--------------|---------------|-------------------|-----------------|
| **Critical** | High          | Critical          | Critical        |
| **High**     | Medium        | High              | Critical        |
| **Medium**   | Low           | Medium            | High            |
| **Low**      | Low           | Low               | Medium          |

---

## Mitigations

| Threat ID | Mitigation | Type | Status | Owner |
|-----------|-----------|------|--------|-------|
| | | Prevent / Detect / Respond | Proposed / Implemented / Verified | |

---

## Residual Risk

Risks that remain after mitigations are applied.

| Threat ID | Residual Risk | Accepted By | Rationale |
|-----------|--------------|-------------|-----------|
| | | | |

---

## Review Schedule

| Next Review | Trigger for Early Review |
|-------------|------------------------|
| YYYY-MM-DD  | Major architecture change, new attack surface, security incident, dependency update |
