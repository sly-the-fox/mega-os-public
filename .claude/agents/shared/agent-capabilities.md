# Agent Capability Taxonomy

Defines structured capability profiles for all Mega-OS agents. Each agent's frontmatter includes a `capabilities:` field referencing this taxonomy. The Router uses these for capability-based routing.

---

## Capability Categories

| Key | Description |
|-----|-------------|
| `analysis` | Analyze data, patterns, trends, metrics |
| `design` | Create architectures, interfaces, structures, plans |
| `implementation` | Write code, scripts, configurations |
| `review` | Evaluate quality, correctness, compliance |
| `writing` | Produce written content (articles, docs, copy) |
| `editing` | Review and refine written content for voice, accuracy, structure |
| `coordination` | Orchestrate agents, manage workflows, track progress |
| `research` | Gather and synthesize information from multiple sources |
| `monitoring` | Detect risks, anomalies, drift, staleness |
| `formatting` | Convert, polish, and format content for publication |

## Domain Tags

| Key | Description |
|-----|-------------|
| `technical` | Code, infrastructure, architecture |
| `business` | Strategy, finance, marketing, sales |
| `content` | Writing, editing, publishing |
| `governance` | Oversight, rules, boundaries, compliance |
| `knowledge` | Documentation, history, organization |
| `evolution` | Improvement, evaluation, self-reflection |

## Strength Levels

| Key | Meaning |
|-----|---------|
| `primary` | Core competency — what the agent was built for |
| `secondary` | Can do this but not the main focus |

## Frontmatter Format

```yaml
---
name: architect
description: ...
tools: read, write, bash
capabilities:
  primary: [design, analysis]
  secondary: [review]
  domain: [technical]
---
```

## Routing Priority

1. **Domain match** — technical task routes to technical domain agents
2. **Primary capability match** — analysis task routes to agents with analysis as primary
3. **Secondary capability match** — fallback if no primary match

Supplements workflow-based routing. Workflows define sequence; capabilities refine agent selection.
