# Workflows

Standard workflow sequences. Not every task requires all steps — skip stages that don't apply.

## Planning Workflow
1. **Planner** — breaks down request into tasks, milestones, dependencies
2. **Router** — assigns tasks to appropriate specialist agents
3. **Governor** — validates scope and constraints
4. **PM** — tracks progress, dependencies, deadlines
5. **Specialists** — execute assigned tasks
6. **QA** — verifies deliverables meet quality gates
7. **Reviewer** — checks correctness, standards, completeness
8. **Documenter** — writes or updates documentation
9. **Historian** — records decisions, outcomes, lessons

## Technical Workflow
1. **Architect** — defines or validates technical approach
2. **Engineer** — implements changes
3. **QA** — tests and verifies
4. **Security-Expert** — reviews security concerns (if relevant)
5. **Reviewer** — final review
6. **DevOps** — handles deployment (if needed)
7. **Documenter** — updates technical docs

## Business Workflow
1. **Strategist** — defines business objective and approach
2. **Marketer / Seller / Financier** — execute in their domains
3. **Reviewer** — validates alignment with strategy
4. **Historian** — records decision and rationale

## Incident Workflow
1. **Debugger** — diagnoses root cause
2. **Security-Expert** — assesses security implications (if security-related)
3. **Engineer** — implements fix
4. **QA** — verifies fix, checks for regressions
5. **Historian** — records incident, root cause, resolution

## Knowledge Workflow
1. **Librarian** — locates and organizes relevant information
2. **Summarizer** — distills into concise summaries
3. **Documenter** — produces formal documentation
4. **Historian** — archives knowledge artifact and context

## When to Use Which Workflow
- **New feature or project:** Planning workflow
- **Code change or bug fix:** Technical workflow (or Incident if production issue)
- **Business decision:** Business workflow
- **Production incident:** Incident workflow
- **Documentation or knowledge task:** Knowledge workflow
- **Simple, bounded task:** Skip directly to the relevant specialist
