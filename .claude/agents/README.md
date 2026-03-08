# Agents Folder

This folder contains all agent role definitions used by the system.

## Purpose

The system is organized into specialized agents with clear responsibilities, boundaries, and handoff patterns. The goal is to create a modular multi-agent environment that is easier to maintain, scale, and improve over time.

## Structure

- `REGISTRY.md` — canonical map of all agents, their purposes, and handoff relationships
- `shared/` — common rules, templates, and collaboration protocols used by all agents
- `governance/` — direction, coordination, scope, and risk agents
- `knowledge/` — memory, retrieval, summarization, and documentation agents
- `technical/` — system design, implementation, testing, debugging, deployment, and security agents
- `business/` — growth, messaging, sales, and financial agents
- `evolution/` — system improvement and measurement agents

## How to Use

1. Start with the registry to understand which agent should be used.
2. Use specialist agents for specialist work.
3. Keep agents within their boundaries.
4. Prefer clean handoffs over role sprawl.
5. Record important outcomes through Historian and Documenter.
6. Use Improver and Evaluator to evolve the system based on evidence.

## Design Philosophy

This is not a collection of random helpers. It is a role-based operating framework.

The system should:
- remain modular
- preserve context intelligently
- route work clearly
- avoid unnecessary overlap
- improve over time without chaos
