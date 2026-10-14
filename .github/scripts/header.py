"""Render the README header: name on the left, last year's contributions as a dot grid on the right.

Writes assets/header-dark.svg and assets/header-light.svg. Needs GITHUB_TOKEN and USERNAME.
"""

import json
import os
import urllib.request
from pathlib import Path

USER = os.environ["USERNAME"]
OUT = Path("assets")
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { contributionCount } } } } } }"""

THEMES = {
    "dark": {"text": "#E6EDF3", "muted": "#7D8590", "empty": "#2D333B", "dot": "#E6EDF3"},
    "light": {"text": "#1F2328", "muted": "#59636E", "empty": "#DDE1E6", "dot": "#1F2328"},
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def fetch_calendar():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def level(count, peak):
    """Map a day's count to 0-4, relative to the busiest day, like GitHub's own graph."""
    if count == 0:
        return 0
    return min(4, 1 + int(3 * count / max(peak, 1)))


def render(cal, t):
    w, h = 1200, 180
    weeks = cal["weeks"]
    peak = max(d["contributionCount"] for wk in weeks for d in wk["contributionDays"])
    step, r = 12.2, 4.4
    gx = w - len(weeks) * step - 8
    gy = 40
    opacity = [1, 0.35, 0.6, 0.82, 1]
    dots = []
    for i, wk in enumerate(weeks):
        col = []
        days = wk["contributionDays"]
        # The first week can start mid-week; push its days down so weekdays stay aligned.
        offset = 7 - len(days) if i == 0 else 0
        for j, d in enumerate(days, start=offset):
            lv = level(d["contributionCount"], peak)
            fill = t["empty"] if lv == 0 else t["dot"]
            col.append(
                f'<circle cx="{gx + i * step:.1f}" cy="{gy + j * step:.1f}" r="{r}" fill="{fill}" fill-opacity="{opacity[lv]}"/>'
            )
        # Columns fade in left to right once, so the grid "writes" itself on page load.
        dots.append(f'<g class="c" style="animation-delay:{i * 18}ms">{"".join(col)}</g>')
    total = f"{cal['totalContributions']:,} contributions in the last year"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<style>
  .c {{ opacity: 0; animation: in .5s ease-out forwards; }}
  @keyframes in {{ to {{ opacity: 1; }} }}
</style>
<text x="0" y="88" font-family="{SANS}" font-size="50" font-weight="600" letter-spacing="-1" fill="{t['text']}">Tanvir Chowdhury</text>
<text x="2" y="126" font-family="{MONO}" font-size="18" fill="{t['muted']}">full-stack &amp; AI engineer · dhaka, bangladesh</text>
{''.join(dots)}
<text x="{w - 8 + r}" y="{gy + 7 * step + 22}" text-anchor="end" font-family="{MONO}" font-size="15" fill="{t['muted']}">{total}</text>
</svg>
"""


def main():
    cal = fetch_calendar()
    OUT.mkdir(exist_ok=True)
    for name, theme in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(render(cal, theme))


if __name__ == "__main__":
    main()
