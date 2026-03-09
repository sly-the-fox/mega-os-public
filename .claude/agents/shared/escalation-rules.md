# Escalation Rules

Structured framework for when and how to escalate decisions, risks, and scope changes.

## Risk Severity Table

| Severity | Definition | Examples | Required Action |
|----------|-----------|----------|-----------------|
| **Critical** | Immediate harm to production, data, or security | Data breach, production outage, credential exposure, data loss | Halt work. Notify Sentinel + Security-Expert. User must approve resolution. |
| **High** | Significant impact if not addressed promptly | Auth bypass, unvalidated external input, deployment to production, major scope expansion | Escalate to relevant specialist. Block until reviewed. |
| **Medium** | Meaningful risk that warrants attention | Performance degradation, missing test coverage, unclear requirements, moderate scope creep | Flag in handoff. Specialist reviews before proceeding. |
| **Low** | Minor concern, addressable in normal flow | Code style issues, minor refactoring opportunities, documentation gaps | Note for future improvement. Do not block work. |

## Scope Change Detection — Governor Triggers

Escalate to Governor when any of these occur:
- Work touches files or systems **not included in the original plan**
- Estimated effort exceeds original estimate by **2x or more**
- New **external dependencies** are introduced (packages, services, APIs)
- **Blast radius expands** beyond the originally scoped components
- An agent is performing work **outside its defined responsibilities**

## Security Escalation — Security-Expert Triggers

Security-Expert review is **mandatory** (not optional) when work touches:
- **Authentication** — login, session, token, OAuth, SSO
- **Cryptography** — encryption, hashing, signing, key management
- **Input validation** — user input, form data, query parameters, file uploads
- **Secrets management** — API keys, credentials, environment variables, certificates
- **API boundaries** — external-facing endpoints, rate limiting, CORS, authorization
- **Third-party data** — handling data from external services or users

## Risk Escalation — Sentinel Triggers

Escalate to Sentinel when:
- Work affects **production systems** or live environments
- **Blast radius** extends beyond the immediate task scope
- **Financial exposure** — pricing changes, payment processing, billing logic
- **Compliance implications** — data privacy, regulatory requirements, audit trails
- **Permission changes** — access control modifications, role changes
- **Irreversible actions** — data deletion, schema migrations, infrastructure teardown

## General Escalation — Overseer Triggers

Escalate to Overseer when:
- **Conflicting requirements** — two valid interpretations that lead to different outcomes
- **Meaningful tradeoffs** — decisions where each option has significant downsides
- **Blocked work** — progress stalled and no agent can unblock independently
- **Boundary violations** — an agent needs to act outside its defined role
- **Resource conflicts** — multiple priorities compete for the same capacity

## Plan-Delivery Mismatch — Auditor Triggers

Escalate to Auditor when:
- **Planned items not delivered** — work items from the approved plan were not implemented
- **Significant plan deviation** — implementation diverges materially from the plan without documented approval
- **Unstated assumptions** discovered post-implementation that affect correctness
- **Layer gaps** — persistence or injection misalignment (results won't survive to future sessions)
- **Scope contraction** — planned work silently dropped without explicit decision

## Overseer vs Governor Conflict Resolution

These two governance agents have adjacent but distinct authority:
- **Governor** enforces scope boundaries (is this within the approved plan?)
- **Overseer** resolves system-level conflicts (which priority wins?)

When they disagree:
1. Governor states scope concern with evidence
2. Overseer states system-level concern with evidence
3. If the issue is purely scope, Governor decides
4. If the issue is cross-cutting priority or resource allocation, Overseer decides
5. If both dimensions apply, Overseer makes the final call (Overseer outranks Governor on system-level decisions)
6. Historian records the resolution

## Escalation Process

1. The escalating agent states the issue clearly with evidence
2. The receiving agent (Governor, Security-Expert, Sentinel, or Overseer) evaluates
3. Decision is made and communicated back to the escalating agent
4. Historian records the escalation and decision if significant
