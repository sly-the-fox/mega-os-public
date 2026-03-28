#!/usr/bin/env python3
"""Fetch product and channel metrics, append to adoption-metrics.md, optionally notify via webhook."""

import argparse
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent.parent
METRICS_FILE = ROOT / "business" / "marketing" / "adoption-metrics.md"

# ---------------------------------------------------------------------------
# Configuration — customize these for your projects
# ---------------------------------------------------------------------------

GITHUB_USER = "<your-github-username>"

PACKAGES = [
    # {"name": "<pypi-package-name>", "section": "<Display Name>", "github": "<owner/repo>"},
]

GITHUB_REPOS = [
    # {"repo": "<owner/repo>", "section": "<Display Name>"},
]

WEBSITES = [
    # "https://your-site.dev",
    # "https://your-app.pages.dev",
]

DEVTO_USERNAME = "<your-devto-username>"

# Optional webhook URL for notifications (Slack, Discord, custom)
WEBHOOK_URL = os.environ.get("METRICS_WEBHOOK_URL", "")

MILESTONE_THRESHOLDS = [100, 250, 500, 1_000, 2_500, 5_000, 10_000]

PYPISTATS_URL = "https://pypistats.org/api/packages/{package}/overall"
GITHUB_API_URL = "https://api.github.com/repos/{repo}"
DEVTO_API_URL = "https://dev.to/api/articles?username={username}&per_page=1000"


def _github_headers() -> dict:
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


# ---------------------------------------------------------------------------
# PyPI
# ---------------------------------------------------------------------------

def fetch_pypi_stats(package: str) -> dict:
    """Fetch recent and total download counts from pypistats.org."""
    try:
        resp = httpx.get(PYPISTATS_URL.format(package=package), timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except (httpx.HTTPError, json.JSONDecodeError) as e:
        print(f"  PyPI fetch failed for {package}: {e}")
        return {"total_with_mirrors": "?", "total_without_mirrors": "?", "recent_daily": "?"}

    rows = data.get("data", [])
    with_mirrors = sum(r["downloads"] for r in rows if r.get("category") == "with_mirrors")
    without_mirrors = sum(r["downloads"] for r in rows if r.get("category") == "without_mirrors")

    daily_rows = sorted(
        [r for r in rows if r.get("category") == "with_mirrors"],
        key=lambda r: r.get("date", ""),
    )
    recent_daily = daily_rows[-1]["downloads"] if daily_rows else "?"

    return {
        "total_with_mirrors": with_mirrors,
        "total_without_mirrors": without_mirrors,
        "recent_daily": recent_daily,
    }


# ---------------------------------------------------------------------------
# GitHub repo info
# ---------------------------------------------------------------------------

def fetch_github_repo(repo: str) -> dict:
    """Fetch repo stats from GitHub API."""
    try:
        resp = httpx.get(GITHUB_API_URL.format(repo=repo), headers=_github_headers(), timeout=15)
        resp.raise_for_status()
        d = resp.json()
        return {
            "stars": d.get("stargazers_count", 0),
            "forks": d.get("forks_count", 0),
            "open_issues": d.get("open_issues_count", 0),
            "watchers": d.get("subscribers_count", 0),
        }
    except (httpx.HTTPError, json.JSONDecodeError) as e:
        print(f"  GitHub fetch failed for {repo}: {e}")
        return {"stars": -1, "forks": -1, "open_issues": -1, "watchers": -1}


# ---------------------------------------------------------------------------
# GitHub traffic (requires push access)
# ---------------------------------------------------------------------------

def fetch_github_traffic(repo: str) -> dict:
    """Fetch clone and view counts via gh CLI."""
    result = {"clones_14d": "?", "views_14d": "?"}
    for kind in ("clones", "views"):
        try:
            proc = subprocess.run(
                ["gh", "api", f"repos/{repo}/traffic/{kind}"],
                capture_output=True, text=True, timeout=15,
            )
            if proc.returncode == 0:
                data = json.loads(proc.stdout)
                result[f"{kind}_14d"] = data.get("count", "?")
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
            pass
    return result


# ---------------------------------------------------------------------------
# GitHub Sponsors
# ---------------------------------------------------------------------------

def fetch_github_sponsors() -> int:
    """Fetch sponsor count via gh GraphQL API."""
    query = '{ viewer { sponsors { totalCount } } }'
    try:
        proc = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={query}"],
            capture_output=True, text=True, timeout=15,
        )
        if proc.returncode == 0:
            data = json.loads(proc.stdout)
            return data.get("data", {}).get("viewer", {}).get("sponsors", {}).get("totalCount", 0)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        pass
    return -1


# ---------------------------------------------------------------------------
# GitHub repo discovery
# ---------------------------------------------------------------------------

def discover_repos() -> list[str]:
    """Auto-detect public repos for the configured user."""
    if GITHUB_USER.startswith("<"):
        return []
    try:
        resp = httpx.get(
            f"https://api.github.com/users/{GITHUB_USER}/repos?type=public&per_page=100",
            headers=_github_headers(), timeout=15,
        )
        resp.raise_for_status()
        return [r["full_name"] for r in resp.json()]
    except (httpx.HTTPError, json.JSONDecodeError) as e:
        print(f"  Repo discovery failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Website availability
# ---------------------------------------------------------------------------

def check_websites(urls: list[str]) -> list[dict]:
    """HEAD-check each URL, return status and response time."""
    results = []
    for url in urls:
        try:
            start = datetime.now()
            resp = httpx.head(url, timeout=10, follow_redirects=True)
            elapsed_ms = int((datetime.now() - start).total_seconds() * 1000)
            results.append({"url": url, "status": resp.status_code, "ms": elapsed_ms, "up": 200 <= resp.status_code < 400})
        except httpx.HTTPError:
            results.append({"url": url, "status": "error", "ms": -1, "up": False})
    return results


# ---------------------------------------------------------------------------
# Dev.to
# ---------------------------------------------------------------------------

def fetch_devto(username: str) -> dict:
    """Fetch aggregate Dev.to stats."""
    if username.startswith("<"):
        return {"views": "?", "reactions": "?", "comments": "?", "articles": "?"}
    try:
        resp = httpx.get(DEVTO_API_URL.format(username=username), timeout=15)
        resp.raise_for_status()
        articles = resp.json()
        total_views = sum(a.get("page_views_count", 0) for a in articles)
        total_reactions = sum(a.get("positive_reactions_count", 0) for a in articles)
        total_comments = sum(a.get("comments_count", 0) for a in articles)
        return {"views": total_views, "reactions": total_reactions, "comments": total_comments, "articles": len(articles)}
    except (httpx.HTTPError, json.JSONDecodeError) as e:
        print(f"  Dev.to fetch failed: {e}")
        return {"views": "?", "reactions": "?", "comments": "?", "articles": "?"}


# ---------------------------------------------------------------------------
# Metrics file writer
# ---------------------------------------------------------------------------

def append_metrics_row(section: str, today: str, row: str):
    """Append a row to the named section in adoption-metrics.md."""
    text = METRICS_FILE.read_text(encoding="utf-8")
    marker = f"## {section}"
    lines = text.split("\n")
    insert_idx = None
    in_section = False

    for i, line in enumerate(lines):
        if marker in line:
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") and marker not in line:
                insert_idx = i
                break
            if line.startswith("---") and i > 0 and not lines[i - 1].startswith("|"):
                insert_idx = i
                break
            if line.startswith("|") or line.startswith("<!--"):
                insert_idx = i + 1

    if insert_idx is None:
        print(f"  Could not find insertion point for {section}")
        return False

    # Skip if an identical row already exists in this section
    section_start = next((i for i, l in enumerate(lines) if marker in l), 0)
    section_end = insert_idx
    for line in lines[section_start:section_end]:
        if row.strip() == line.strip():
            print(f"  {section}: identical entry already exists, skipping")
            return False

    lines.insert(insert_idx, row)
    METRICS_FILE.write_text("\n".join(lines), encoding="utf-8")
    return True


def ensure_section(section: str, headers: str):
    """Ensure a section exists in adoption-metrics.md; create if missing."""
    text = METRICS_FILE.read_text(encoding="utf-8")
    if f"## {section}" in text:
        return
    text += f"\n---\n\n## {section}\n\n{headers}\n<!-- Entries appended automatically -->\n"
    METRICS_FILE.write_text(text, encoding="utf-8")
    print(f"  Created new section: {section}")


# ---------------------------------------------------------------------------
# Milestone detection
# ---------------------------------------------------------------------------

def check_milestones(label: str, metric_name: str, value, thresholds=None) -> list[str]:
    """Check if value crosses any milestone thresholds."""
    if thresholds is None:
        thresholds = MILESTONE_THRESHOLDS
    milestones = []
    if isinstance(value, int) and value > 0:
        for t in thresholds:
            if value >= t:
                milestones.append(f"{label}: {t}+ {metric_name}!")
        # First-ever detection
        if value == 1:
            milestones.append(f"{label}: first {metric_name}!")
    return milestones


# ---------------------------------------------------------------------------
# Webhook notification (optional)
# ---------------------------------------------------------------------------

def notify_webhook(message: str):
    """Send notification via webhook (Slack, Discord, or custom)."""
    if not WEBHOOK_URL:
        print("  No METRICS_WEBHOOK_URL configured, skipping notification")
        return
    try:
        httpx.post(WEBHOOK_URL, json={"text": message, "content": message}, timeout=10)
        print("  Notification sent via webhook")
    except httpx.HTTPError as e:
        print(f"  Webhook notification failed: {e}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fetch product and channel metrics")
    parser.add_argument("--notify", action="store_true", help="Send webhook notification")
    parser.add_argument("--products-only", action="store_true", help="Skip channel metrics")
    parser.add_argument("--channels-only", action="store_true", help="Skip product metrics")
    args = parser.parse_args()

    today = date.today().isoformat()
    print(f"Fetching metrics for {today}")

    if not PACKAGES and not GITHUB_REPOS and not WEBSITES:
        print("\nNo sources configured. Edit the PACKAGES, GITHUB_REPOS, and WEBSITES")
        print("lists at the top of this script to add your projects.")
        sys.exit(0)

    results = []
    milestones = []

    # ---- Products ----
    if not args.channels_only:
        for pkg in PACKAGES:
            print(f"\n--- {pkg['section']} --- PyPI ---")
            pypi = fetch_pypi_stats(pkg["name"])
            print(f"  PyPI total: {pypi['total_with_mirrors']}, daily: {pypi['recent_daily']}")

            repo_info = fetch_github_repo(pkg["github"])
            print(f"  GitHub stars: {repo_info['stars']}, forks: {repo_info['forks']}")

            stars_str = str(repo_info["stars"]) if repo_info["stars"] >= 0 else "?"
            total = pypi["total_with_mirrors"]
            recent = pypi["recent_daily"]
            without = pypi["total_without_mirrors"]
            notes = f"with_mirrors: {total}, without_mirrors: {without}"
            row = f"| {today} | ~{total} | {recent}/day | {stars_str} | {notes} |"
            append_metrics_row(f"{pkg['section']} --- PyPI & GitHub", today, row)

            results.append(f"{pkg['section']}: ~{total} downloads, {stars_str} stars, {repo_info['forks']} forks")

            # Milestones
            if isinstance(total, int):
                milestones.extend(check_milestones(pkg["name"], "downloads", total))
            milestones.extend(check_milestones(pkg["name"], "GitHub stars", repo_info["stars"]))
            milestones.extend(check_milestones(pkg["name"], "forks", repo_info["forks"]))

        # GitHub-only repos (no PyPI)
        for r in GITHUB_REPOS:
            if any(r["repo"] == p.get("github") for p in PACKAGES):
                continue  # Already covered above
            section = f"{r['section']} --- GitHub"
            print(f"\n--- {section} ---")
            ensure_section(section,
                           "| Date | Stars | Forks | Open Issues | Watchers | Notes |\n|------|-------|-------|-------------|----------|-------|")
            info = fetch_github_repo(r["repo"])
            if info["stars"] >= 0:
                row = f"| {today} | {info['stars']} | {info['forks']} | {info['open_issues']} | {info['watchers']} | |"
                append_metrics_row(section, today, row)
                results.append(f"{r['section']}: {info['stars']} stars, {info['forks']} forks")
                milestones.extend(check_milestones(r["repo"], "stars", info["stars"]))

        # GitHub traffic
        print("\n--- GitHub Traffic ---")
        ensure_section("GitHub Traffic",
                       "| Date | Repo | Clones (14d) | Views (14d) | Notes |\n|------|------|-------------|-------------|-------|")
        for r in GITHUB_REPOS:
            traffic = fetch_github_traffic(r["repo"])
            print(f"  {r['repo']}: clones={traffic['clones_14d']}, views={traffic['views_14d']}")
            row = f"| {today} | {r['repo']} | {traffic['clones_14d']} | {traffic['views_14d']} | |"
            append_metrics_row("GitHub Traffic", today, row)

        # GitHub Sponsors
        print("\n--- GitHub Sponsors ---")
        ensure_section("GitHub Sponsors",
                       "| Date | Sponsor Count | Notes |\n|------|--------------|-------|")
        sponsors = fetch_github_sponsors()
        print(f"  Sponsors: {sponsors}")
        if sponsors >= 0:
            row = f"| {today} | {sponsors} | |"
            append_metrics_row("GitHub Sponsors", today, row)
            milestones.extend(check_milestones("GitHub Sponsors", "sponsors", sponsors))

    # ---- Website Availability ----
    if not args.products_only and not args.channels_only:
        print("\n--- Website Availability ---")
        ensure_section("Website Availability",
                       "| Date | Site | Status | Response (ms) | Notes |\n|------|------|--------|---------------|-------|")
        site_results = check_websites(WEBSITES)
        for s in site_results:
            status_emoji = "up" if s["up"] else "DOWN"
            host = s["url"].replace("https://", "").rstrip("/")
            print(f"  {host}: {status_emoji} ({s['status']}, {s['ms']}ms)")
            row = f"| {today} | {host} | {s['status']} | {s['ms']} | {status_emoji} |"
            append_metrics_row("Website Availability", today, row)
            if not s["up"]:
                results.append(f"SITE DOWN: {host}")

    # ---- Dev.to ----
    if not args.products_only:
        print("\n--- Dev.to ---")
        devto = fetch_devto(DEVTO_USERNAME)
        print(f"  Views: {devto['views']}, Reactions: {devto['reactions']}, Comments: {devto['comments']}, Articles: {devto['articles']}")
        if devto["views"] != "?":
            row = f"| {today} | {devto['views']} | {devto['reactions']} | {devto['comments']} | {devto['articles']} articles |"
            append_metrics_row("Dev.to", today, row)
            results.append(f"Dev.to: {devto['views']} views, {devto['reactions']} reactions")

    # ---- Repo Discovery ----
    if not args.channels_only:
        print("\n--- Repo Discovery ---")
        known = {r["repo"] for r in GITHUB_REPOS}
        discovered = discover_repos()
        new_repos = [r for r in discovered if r not in known]
        if new_repos:
            print(f"  New public repos found: {', '.join(new_repos)}")
            results.append(f"New repos: {', '.join(new_repos)}")
        else:
            print(f"  No new repos ({len(discovered)} total)")

    # ---- Deduplicate milestones (keep highest per label) ----
    seen = set()
    unique_milestones = []
    for m in reversed(milestones):
        key = m.split(":")[0]
        if key not in seen:
            seen.add(key)
            unique_milestones.append(m)
    unique_milestones.reverse()

    # ---- Build summary ----
    msg = f"Daily Metrics Scan ({today})\n" + "\n".join(results)
    if unique_milestones:
        msg += "\n\nMilestones:\n" + "\n".join(f"  {m}" for m in unique_milestones)

    print(f"\n{'='*50}")
    print(msg)

    if args.notify:
        notify_webhook(msg)

    print("\nDone.")


if __name__ == "__main__":
    main()
