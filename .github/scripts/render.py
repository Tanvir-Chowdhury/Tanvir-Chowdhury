"""Render every SVG card used by the profile README into assets/.

The hero card is drawn from the live contribution calendar, so this runs in CI
(needs GITHUB_TOKEN and USERNAME). All other cards are static copy defined below.
GitHub proxies README images and strips scripts, so cards use system fonts and
CSS/SMIL animation only.
"""

import base64
import json
import os
import sys
import urllib.request
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

USER = os.environ["USERNAME"]
OUT = Path("assets")

# Design tokens: one neutral ramp, one accent, per-card hues used sparingly.
BG = "#09090B"
CARD = "#0F0F12"
LINE = "#27272A"
TEXT = "#FAFAFA"
MUTED = "#A1A1AA"
DIM = "#71717A"
ACCENT = "#A78BFA"
GREEN = "#4ADE80"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { contributionCount date } } } } } }"""


def fetch_calendar():
    body = json.dumps({"query": QUERY, "variables": {"login": USER}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def frame(w, h, body, style="", defs="", glow=None):
    """Card shell: rounded dark panel, hairline border, optional soft accent glow in one corner."""
    glow_el = ""
    if glow:
        color, gx, gy = glow
        glow_el = f'<circle cx="{gx}" cy="{gy}" r="220" fill="{color}" opacity="0.16" filter="url(#g)"/>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
  <filter id="g" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="80"/></filter>
  <clipPath id="clip"><rect width="{w}" height="{h}" rx="20"/></clipPath>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff" stop-opacity="0"/><stop offset="0.5" stop-color="#ffffff" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
  {defs}
</defs>
<style>
  text {{ font-family: {SANS}; }}
  .m {{ font-family: {MONO}; }}
  {style}
</style>
<g clip-path="url(#clip)">
  <rect width="{w}" height="{h}" fill="{CARD}"/>
  {glow_el}
  <rect x="{w * 0.15}" y="0" width="{w * 0.7}" height="1" fill="url(#edge)"/>
  {body}
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="19.5" stroke="{LINE}"/>
</svg>
"""


def shot(name):
    """Screenshot as a data URI: GitHub's image proxy blocks external URLs inside SVGs."""
    data = base64.b64encode((OUT / "shots" / f"{name}.jpg").read_bytes()).decode()
    return f"data:image/jpeg;base64,{data}"


def window(x, y, w, img, aspect, title, uid):
    """Screenshot inside a minimal app-window frame. Returns (markup, height)."""
    bar = 34
    ih = w * aspect
    h = bar + ih
    return f"""
<rect x="{x}" y="{y + 18}" width="{w}" height="{h}" rx="14" fill="#000" opacity="0.5" filter="url(#sh)"/>
<clipPath id="win{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/></clipPath>
<g clip-path="url(#win{uid})">
  <rect x="{x}" y="{y}" width="{w}" height="{bar}" fill="#18181B"/>
  <circle cx="{x + 20}" cy="{y + bar / 2}" r="5" fill="#3F3F46"/><circle cx="{x + 37}" cy="{y + bar / 2}" r="5" fill="#3F3F46"/><circle cx="{x + 54}" cy="{y + bar / 2}" r="5" fill="#3F3F46"/>
  <text x="{x + w / 2}" y="{y + bar / 2 + 4.5}" text-anchor="middle" font-size="12.5" fill="{DIM}">{escape(title)}</text>
  <image href="{img}" x="{x}" y="{y + bar}" width="{w}" height="{ih}" preserveAspectRatio="xMidYMin slice"/>
</g>
<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="11.5" stroke="#ffffff" stroke-opacity="0.1"/>
""", h


def eyebrow(x, y, label, color=DIM):
    return f'<text class="m" x="{x}" y="{y}" font-size="13" letter-spacing="2" fill="{color}">{escape(label.upper())}</text>'


def streaks(days):
    """Longest run of active days, and the run ending today (or yesterday, if today is still empty)."""
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    current = 0
    tail = days[:-1] if days and not days[-1]["contributionCount"] else days
    for d in reversed(tail):
        if not d["contributionCount"]:
            break
        current += 1
    return longest, current


def hero(cal):
    w, h = 1200, 440
    weeks = cal["weeks"]
    days = [d for wk in weeks for d in wk["contributionDays"]]
    peak = max(d["contributionCount"] for d in days) or 1
    longest, current = streaks(days)
    active = sum(1 for d in days if d["contributionCount"])

    step, r = 9.6, 3.4
    gx, gy = w - 56 - (len(weeks) - 1) * step, 104
    dots = []
    for i, wk in enumerate(weeks):
        cells = wk["contributionDays"]
        offset = 7 - len(cells) if i == 0 else 0  # first week may start mid-week
        col = []
        for j, d in enumerate(cells, start=offset):
            c = d["contributionCount"]
            if c == 0:
                col.append(f'<circle cx="{gx + i * step:.1f}" cy="{gy + j * step:.1f}" r="{r}" fill="#ffffff" fill-opacity="0.06"/>')
                continue
            t = min(1, c / peak)
            op = 0.35 + 0.65 * t ** 0.6
            col.append(f'<circle cx="{gx + i * step:.1f}" cy="{gy + j * step:.1f}" r="{r}" fill="{ACCENT}" fill-opacity="{op:.2f}"/>')
        dots.append(f'<g class="col" style="animation-delay:{i * 16}ms">{"".join(col)}</g>')

    grid_bottom = gy + 6 * step
    stats = [(f"{cal['totalContributions']:,}", "contributions"), (str(active), "active days"), (str(longest), "day best streak")]
    sx = gx - r
    stat_el = []
    for k, (num, label) in enumerate(stats):
        x = sx + k * 168
        stat_el.append(
            f'<text x="{x}" y="{grid_bottom + 62}" font-size="30" font-weight="600" fill="{TEXT}" letter-spacing="-0.5">{num}</text>'
            f'<text class="m" x="{x}" y="{grid_bottom + 86}" font-size="12" fill="{DIM}" letter-spacing="0.5">{label}</text>'
        )
    if current:
        stat_el.append(
            f'<text class="m" x="{w - 56}" y="78" text-anchor="end" font-size="12" fill="{DIM}">'
            f'<tspan fill="{GREEN}">●</tspan> {current}-day streak running</text>'
        )

    body = f"""
<rect width="{w}" height="{h}" fill="url(#dots)" opacity="0.5"/>
{eyebrow(56, 78, "Last 12 months on GitHub").replace(f'x="56"', f'x="{gx - r}"')}
<g>
  <rect x="56" y="58" width="236" height="32" rx="16" fill="{GREEN}" fill-opacity="0.08" stroke="{GREEN}" stroke-opacity="0.3"/>
  <circle cx="76" cy="74" r="4" fill="{GREEN}"/><circle cx="76" cy="74" r="4" fill="{GREEN}" class="ping"/>
  <text class="m" x="90" y="78.5" font-size="12" letter-spacing="1.5" fill="{GREEN}">OPEN FOR FREELANCE</text>
</g>
<text x="54" y="172" font-size="62" font-weight="650" letter-spacing="-2.2" fill="{TEXT}">Tanvir</text>
<text x="54" y="238" font-size="62" font-weight="650" letter-spacing="-2.2" fill="url(#name)">Chowdhury</text>
<text x="56" y="286" font-size="20" fill="{MUTED}">Full-stack &amp; AI engineer. I build backends,</text>
<text x="56" y="314" font-size="20" fill="{MUTED}">LLM features and the occasional desktop app.</text>
<rect x="56" y="354" width="{gx - 120}" height="1" fill="{LINE}"/>
<text class="m" x="56" y="388" font-size="13" fill="{DIM}">Python · TypeScript · Django · FastAPI · React · Vue · Postgres</text>
<text class="m" x="56" y="410" font-size="13" fill="{DIM}">Dhaka, Bangladesh · remote</text>
{''.join(dots)}
{''.join(stat_el)}
"""
    defs = f"""
  <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#ffffff" fill-opacity="0.05"/></pattern>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{TEXT}"/><stop offset="1" stop-color="{ACCENT}"/>
  </linearGradient>"""
    style = """
  .col { opacity: 0; animation: in .6s ease-out forwards; }
  @keyframes in { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
  .ping { transform-box: fill-box; transform-origin: center; animation: ping 2s ease-out infinite; }
  @keyframes ping { from { transform: scale(1); opacity: .7; } to { transform: scale(3.2); opacity: 0; } }"""
    return frame(w, h, body, style, defs, glow=(ACCENT, 1050, 40))


def lucentedit():
    """Featured project: copy on top, a real screenshot of a design made through its MCP tools below."""
    w = 1200
    chips = ["MCP server built in", "macOS · Windows · Linux", "MIT licensed"]
    cx, chip_el = w - 56, []
    for c in reversed(chips):
        cw = len(c) * 8.2 + 28
        cx -= cw
        chip_el.append(f'<rect x="{cx}" y="118" width="{cw}" height="32" rx="16" fill="#ffffff" fill-opacity="0.04" stroke="{LINE}"/>'
                       f'<text class="m" x="{cx + cw / 2}" y="138.5" text-anchor="middle" font-size="13" fill="{MUTED}">{escape(c)}</text>')
        cx -= 10
    win, wh = window(56, 236, w - 112, shot("lucentedit"), 1672 / 2880, "LucentEdit — Brew Day launch", "le")
    h = int(236 + wh + 92)
    body = f"""
{eyebrow(56, 72, "Now building · open source", ACCENT)}
<text x="54" y="134" font-size="48" font-weight="650" letter-spacing="-1.6" fill="{TEXT}">LucentEdit</text>
<text x="56" y="178" font-size="20" fill="{MUTED}">A free, lightweight Photoshop and Illustrator alternative that AI agents can drive over MCP.</text>
{''.join(chip_el)}
{win}
<text class="m" x="56" y="{h - 40}" font-size="13" fill="{DIM}">Every layer above was created by an agent through LucentEdit's MCP tools: new_document, add_shape, add_text.</text>
"""
    return frame(w, h, body, glow=("#F472B6", 1100, 300))


def shot_card(kind, title, desc, stack, color, img, aspect, uid):
    w = 590
    win, wh = window(32, 32, w - 64, shot(img), aspect, title, uid)
    top = 32 + wh + 54
    lines = wrap(desc, 48)
    text = "".join(f'<text x="34" y="{top + 76 + i * 27}" font-size="18" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(lines))
    h = int(top + 76 + 2 * 27 + 62)
    body = f"""
{win}
<rect x="34" y="{top - 10}" width="10" height="10" rx="2" fill="{color}"/>
{eyebrow(54, top, kind)}
<text x="{w - 34}" y="{top + 2}" text-anchor="end" font-size="20" fill="{DIM}">↗</text>
<text x="32" y="{top + 44}" font-size="30" font-weight="650" letter-spacing="-0.8" fill="{TEXT}">{escape(title)}</text>
{text}
<text class="m" x="34" y="{h - 34}" font-size="13" fill="{DIM}">{escape(stack)}</text>
"""
    return frame(w, h, body, glow=(color, w, 0))


SHOT_CARDS = [
    ("webshield", "Security · SaaS", "WebShield AI",
     "Catches SQL injection, XSS and defacement on live sites and alerts the owner in real time.",
     "FastAPI · Vue · TensorFlow · Postgres", "#38BDF8", "webshield", 0.46),
    ("nsu-csms", "Scheduling · AI", "NSU Class Scheduler",
     "Auto-schedules classes across rooms and teachers, with an AI assistant for students.",
     "FastAPI · React · Postgres · Mistral", ACCENT, "nsu-csms", 0.46),
    ("streamflex", "Streaming platform", "StreamFlex",
     "Movie streaming with subscriptions, purchases and an admin panel for the catalogue.",
     "PHP · MySQL", "#F87171", "streamflex", 0.46),
]

MORE = [
    ("Phoenix", "Telegram tutor for an admission coaching company", "Python · OpenAI", "#FB923C"),
    ("RAG Chatbot API", "Chat API that answers from your documents", "Django REST · Pinecone", ACCENT),
    ("BD Phone Guard", "WordPress plugin that cleans phone numbers", "PHP · WordPress", GREEN),
]


def more_card(h):
    """Text-only companion card for projects without a UI to screenshot, sized to match its neighbour."""
    w = 590
    rows = []
    row_h = (h - 120) / len(MORE)
    for i, (name, desc, stack, color) in enumerate(MORE):
        y = 104 + i * row_h
        rows.append(f"""
<rect x="34" y="{y + 18}" width="10" height="10" rx="2" fill="{color}"/>
<text x="56" y="{y + 30}" font-size="24" font-weight="650" letter-spacing="-0.5" fill="{TEXT}">{escape(name)}</text>
<text x="34" y="{y + 64}" font-size="18" fill="{MUTED}">{escape(desc)}</text>
<text class="m" x="34" y="{y + 92}" font-size="13" fill="{DIM}">{escape(stack)}</text>""")
        if i:
            rows.append(f'<rect x="34" y="{y - 8}" width="{w - 68}" height="1" fill="{LINE}"/>')
    body = f"""{eyebrow(34, 66, "AI, bots & plugins")}{''.join(rows)}"""
    return frame(w, int(h), body, glow=(ACCENT, w, h))


QUOTES = [
    ("Tanvir built a great website for me last time. That's exactly why I came back for my next project.", "Ahein", "Returning client"),
    ("He's done a great job with our marketing and played a big part in bringing in more sales.", "CEO", "Phoenix Education & Automata One"),
    ("He really knows his craft. He built great websites for me, and for my friends too.", "Rahat Hassan", "Client"),
]


def clients():
    w, h = 1200, 260
    col_w = (w - 112) / 3
    cols = []
    for i, (q, name, role) in enumerate(QUOTES):
        x = 56 + i * col_w
        lines = wrap(q, 34)
        qt = "".join(f'<text x="{x}" y="{112 + k * 27}" font-size="18" fill="{TEXT}" fill-opacity="0.9">{escape(l)}</text>' for k, l in enumerate(lines))
        cols.append(f"""{qt}
<text x="{x}" y="{h - 44}" font-size="15" font-weight="600" fill="{TEXT}">{escape(name)}</text>
<text x="{x}" y="{h - 24}" font-size="13" fill="{DIM}">{escape(role)}</text>""")
        if i:
            cols.append(f'<rect x="{x - 28}" y="96" width="1" height="{h - 136}" fill="{LINE}"/>')
    body = f"""{eyebrow(56, 66, "What clients say")}{''.join(cols)}"""
    return frame(w, h, body)


def contact():
    w, h = 1200, 200
    body = f"""
{eyebrow(56, 70, "Have something in mind?")}
<text x="54" y="128" font-size="40" font-weight="650" letter-spacing="-1.2" fill="{TEXT}">Let's build it together.</text>
<text x="56" y="164" font-size="18" fill="{MUTED}">Freelance, contract or full-time. Tell me what you're building.</text>
<rect x="{w - 296}" y="72" width="240" height="56" rx="28" fill="{TEXT}"/>
<text x="{w - 176}" y="106" text-anchor="middle" font-size="18" font-weight="600" fill="{BG}">Email me  →</text>
"""
    return frame(w, h, body, glow=(ACCENT, 1100, 200))


def main():
    OUT.mkdir(exist_ok=True)
    files = {"hero.svg": hero(fetch_calendar())}
    # Static cards embed screenshots and only change when the copy does, so CI skips them.
    if "--all" in sys.argv:
        files["lucentedit.svg"] = lucentedit()
        files["clients.svg"] = clients()
        files["contact.svg"] = contact()
        for key, *args in SHOT_CARDS:
            svg = shot_card(*args, uid=key)
            files[f"work-{key}.svg"] = svg
        last_h = float(files["work-streamflex.svg"].split('height="', 1)[1].split('"', 1)[0])
        files["work-more.svg"] = more_card(last_h)
    for name, svg in files.items():
        (OUT / name).write_text(svg)


if __name__ == "__main__":
    main()
