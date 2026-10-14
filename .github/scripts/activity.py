"""Rewrite the README activity block from the owner's recent public GitHub events."""

import json
import os
import re
import urllib.request
from datetime import datetime

USER = os.environ["USERNAME"]
MAX_LINES = 5
START, END = "<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->"


def fetch_events():
    req = urllib.request.Request(
        f"https://api.github.com/users/{USER}/events/public?per_page=100",
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Accept": "application/vnd.github+json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def describe(e):
    """One markdown line per event, or None for event types we skip."""
    repo = e["repo"]["name"]
    if repo == f"{USER}/{USER}":
        return None  # the profile repo's own bot commits are noise
    link = f"[{repo.split('/')[1]}](https://github.com/{repo})"
    p, t = e["payload"], e["type"]
    if t == "PushEvent":
        # The events API does not always include commit counts, so only show one when present.
        n = p.get("size") or len(p.get("commits") or [])
        return f"Pushed {n} commit{'s' if n > 1 else ''} to {link}" if n else f"Pushed to {link}"
    if t == "CreateEvent" and p.get("ref_type") == "repository":
        return f"Created {link}"
    if t == "ReleaseEvent":
        return f"Released {p['release']['tag_name']} of {link}"
    if t == "PullRequestEvent" and p.get("action") in ("opened", "closed"):
        verb = "Merged" if p["pull_request"].get("merged") else p["action"].capitalize()
        return f"{verb} PR #{p['number']} in {link}"
    if t == "IssuesEvent" and p.get("action") == "opened":
        return f"Opened issue #{p['issue']['number']} in {link}"
    if t == "WatchEvent":
        return f"Starred {link}"
    return None


def main():
    lines, seen = [], set()
    # The events API is not strictly ordered, so sort newest first ourselves.
    for e in sorted(fetch_events(), key=lambda e: e["created_at"], reverse=True):
        text = describe(e)
        if not text:
            continue
        day = datetime.fromisoformat(e["created_at"].replace("Z", "+00:00")).strftime("%b %d")
        # Collapse repeated pushes to the same repo into its most recent entry.
        key = (e["type"], e["repo"]["name"])
        if e["type"] == "PushEvent" and key in seen:
            continue
        seen.add(key)
        lines.append(f"- {text} <sub>{day}</sub>")
        if len(lines) == MAX_LINES:
            break
    block = START + "\n" + "\n".join(lines) + "\n" + END
    with open("README.md") as f:
        readme = f.read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, readme, flags=re.S)
    if new != readme:
        with open("README.md", "w") as f:
            f.write(new)


if __name__ == "__main__":
    main()
