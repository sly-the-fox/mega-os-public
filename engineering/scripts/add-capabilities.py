#!/usr/bin/env python3
"""Add capability profiles to all 39 agent definition frontmatter.

Usage: python3 engineering/scripts/add-capabilities.py
"""

import os
import re
import sys

CAPABILITIES = {
    # Governance (9)
    "overseer": {"primary": ["coordination"], "secondary": ["analysis", "monitoring"], "domain": ["governance"]},
    "governor": {"primary": ["monitoring", "review"], "secondary": ["coordination"], "domain": ["governance"]},
    "router": {"primary": ["coordination", "analysis"], "secondary": [], "domain": ["governance"]},
    "planner": {"primary": ["design", "analysis"], "secondary": ["coordination", "research"], "domain": ["governance"]},
    "pm": {"primary": ["coordination", "monitoring"], "secondary": ["analysis"], "domain": ["governance"]},
    "operator": {"primary": ["design", "coordination"], "secondary": ["writing"], "domain": ["governance", "business"]},
    "sentinel": {"primary": ["monitoring", "analysis"], "secondary": ["review"], "domain": ["governance"]},
    "auditor": {"primary": ["review", "analysis"], "secondary": ["research", "monitoring"], "domain": ["governance"]},
    "custodian": {"primary": ["monitoring", "review"], "secondary": ["coordination"], "domain": ["governance", "knowledge"]},
    # Knowledge (7)
    "historian": {"primary": ["writing", "coordination"], "secondary": ["analysis"], "domain": ["knowledge"]},
    "librarian": {"primary": ["coordination", "analysis"], "secondary": ["research"], "domain": ["knowledge"]},
    "summarizer": {"primary": ["writing", "analysis"], "secondary": [], "domain": ["knowledge", "content"]},
    "documenter": {"primary": ["writing"], "secondary": ["research"], "domain": ["knowledge"]},
    "polisher": {"primary": ["formatting"], "secondary": ["editing"], "domain": ["knowledge", "content"]},
    "writer": {"primary": ["writing", "research"], "secondary": ["analysis"], "domain": ["content"]},
    "editor": {"primary": ["editing", "review"], "secondary": ["writing"], "domain": ["content"]},
    # Technical (11)
    "architect": {"primary": ["design", "analysis"], "secondary": ["review"], "domain": ["technical"]},
    "engineer": {"primary": ["implementation"], "secondary": ["design", "analysis"], "domain": ["technical"]},
    "executor": {"primary": ["implementation", "coordination"], "secondary": [], "domain": ["technical"]},
    "reviewer": {"primary": ["review"], "secondary": ["analysis"], "domain": ["technical"]},
    "qa": {"primary": ["review", "analysis"], "secondary": ["implementation"], "domain": ["technical"]},
    "debugger": {"primary": ["analysis", "implementation"], "secondary": ["research"], "domain": ["technical"]},
    "devops": {"primary": ["implementation", "design"], "secondary": ["monitoring"], "domain": ["technical"]},
    "security-expert": {"primary": ["review", "analysis", "monitoring"], "secondary": ["design", "research"], "domain": ["technical", "governance"]},
    "designer": {"primary": ["design"], "secondary": ["analysis", "review"], "domain": ["technical", "content"]},
    "visual-designer": {"primary": ["design", "implementation"], "secondary": ["review"], "domain": ["technical", "content"]},
    "api-designer": {"primary": ["design", "review"], "secondary": ["analysis"], "domain": ["technical"]},
    # Business (8)
    "strategist": {"primary": ["analysis", "design"], "secondary": ["research", "writing"], "domain": ["business"]},
    "marketer": {"primary": ["writing", "design"], "secondary": ["analysis", "research"], "domain": ["business", "content"]},
    "seller": {"primary": ["writing", "analysis"], "secondary": ["coordination"], "domain": ["business"]},
    "financier": {"primary": ["analysis"], "secondary": ["review", "monitoring"], "domain": ["business"]},
    "proposal-writer": {"primary": ["writing"], "secondary": ["analysis", "research"], "domain": ["business", "content"]},
    "client-manager": {"primary": ["coordination", "monitoring"], "secondary": ["writing"], "domain": ["business"]},
    "content-strategist": {"primary": ["design", "analysis"], "secondary": ["writing", "research"], "domain": ["business", "content"]},
    "growth-hacker": {"primary": ["analysis", "implementation"], "secondary": ["research", "writing"], "domain": ["business"]},
    # Evolution (4)
    "evaluator": {"primary": ["analysis", "monitoring"], "secondary": ["review"], "domain": ["evolution"]},
    "improver": {"primary": ["analysis", "design"], "secondary": ["research"], "domain": ["evolution"]},
    "coherence": {"primary": ["analysis"], "secondary": ["review"], "domain": ["evolution"]},
    "parallax": {"primary": ["analysis", "writing"], "secondary": [], "domain": ["evolution"]},
}

AGENT_DIRS = ["governance", "knowledge", "technical", "business", "evolution"]
SKIP_FILES = {"README.md", "REGISTRY.md"}


def yaml_list(items):
    return "[]" if not items else "[" + ", ".join(items) + "]"


def process_file(filepath, agent_name):
    with open(filepath, "r") as f:
        content = f.read()

    m = re.match(r"^---\n(.*?\n)---\n?(.*)", content, re.DOTALL)
    if not m:
        return False

    fm = m.group(1)
    body = m.group(2)

    if agent_name not in CAPABILITIES:
        return False

    # Remove existing capabilities block
    lines = fm.split("\n")
    cleaned = []
    in_caps = False
    for line in lines:
        if line.startswith("capabilities:"):
            in_caps = True
            continue
        if in_caps and (line.startswith("  ") or line.strip() == ""):
            continue
        in_caps = False
        cleaned.append(line)
    fm = "\n".join(cleaned)
    if not fm.endswith("\n"):
        fm += "\n"

    caps = CAPABILITIES[agent_name]
    fm += f"capabilities:\n"
    fm += f"  primary: {yaml_list(caps['primary'])}\n"
    fm += f"  secondary: {yaml_list(caps['secondary'])}\n"
    fm += f"  domain: {yaml_list(caps['domain'])}\n"

    with open(filepath, "w") as f:
        f.write("---\n" + fm + "---\n" + body)
    return True


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(os.path.dirname(script_dir))
    agents_base = os.path.join(repo_root, ".claude", "agents")

    updated = 0
    for subdir in AGENT_DIRS:
        dir_path = os.path.join(agents_base, subdir)
        if not os.path.isdir(dir_path):
            continue
        for fn in sorted(os.listdir(dir_path)):
            if not fn.endswith(".md") or fn in SKIP_FILES:
                continue
            fp = os.path.join(dir_path, fn)
            if os.path.isdir(fp):
                continue
            name = fn[:-3]
            if process_file(fp, name):
                updated += 1
                print(f"  + {subdir}/{fn}")

    print(f"\nUpdated: {updated} / {len(CAPABILITIES)} agents")
    if updated != len(CAPABILITIES):
        missing = set(CAPABILITIES) - {fn[:-3] for sd in AGENT_DIRS
                                        for fn in os.listdir(os.path.join(agents_base, sd))
                                        if fn.endswith(".md") and fn not in SKIP_FILES}
        if missing:
            print(f"Missing: {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
