"""Generate the custom SVG artwork used by the profile README.

Run `python3 assets/build.py` after editing any text below; every SVG in
assets/ is rewritten. SVGs use only system fonts and CSS/SMIL animation,
because GitHub serves README images through a proxy that blocks scripts
and external resources.
"""

import re
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

# Shared palette and font stacks.
BG = "#0A0A12"
CARD = "#10101C"
BORDER = "#26263D"
TEXT = "#ECECF5"
MUTED = "#9B9BB4"
VIOLET = "#8B5CF6"
PURPLE = "#A78BFA"
CYAN = "#22D3EE"
PINK = "#F472B6"
GREEN = "#34D399"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', 'Cascadia Code', Consolas, 'Liberation Mono', Menlo, monospace"


def svg(w, h, body, extra_defs="", style=""):
    """Wrap body in a root <svg> with the shared gradients and fonts."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset="0.5" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>
  </linearGradient>
  <linearGradient id="cardbg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#14142A"/><stop offset="1" stop-color="{CARD}"/>
  </linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" stroke="#ffffff" stroke-opacity="0.035"/>
  </pattern>
  {extra_defs}
</defs>
<style>
  text {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  {style}
</style>
{body}
</svg>
"""


def pill(x, y, label, color=PURPLE, size=13, pad=12, mono=True):
    """Rounded tag chip; returns (markup, width) so callers can lay out rows."""
    w = int(len(label) * size * 0.62) + pad * 2
    cls = ' class="mono"' if mono else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{size + 14}" rx="{(size + 14) / 2}" '
        f'fill="{color}" fill-opacity="0.10" stroke="{color}" stroke-opacity="0.35"/>'
        f'<text{cls} x="{x + w / 2}" y="{y + size + 3}" text-anchor="middle" font-size="{size}" '
        f'fill="{color}">{escape(label)}</text>',
        w,
    )


def pill_row(x, y, labels, colors, size=13, gap=8):
    out = []
    for i, label in enumerate(labels):
        m, w = pill(x, y, label, colors[i % len(colors)], size)
        out.append(m)
        x += w + gap
    return "".join(out)


def hero():
    w, h = 1200, 440
    tags = ["Django", "FastAPI", "React", "Vue", "RAG", "LLMs", "MCP", "PostgreSQL"]
    code = [
        ("<tspan fill='#C084FC'>const</tspan> <tspan fill='#7DD3FC'>tanvir</tspan> = {", 0),
        ("role: <tspan fill='#86EFAC'>'Full-Stack &amp; AI Engineer'</tspan>,", 1),
        ("ships: <tspan fill='#86EFAC'>'production-ready'</tspan>,", 1),
        ("stack: [<tspan fill='#86EFAC'>'Python'</tspan>, <tspan fill='#86EFAC'>'TS'</tspan>, <tspan fill='#86EFAC'>'AI'</tspan>],", 1),
        ("loves: <tspan fill='#86EFAC'>'hard problems'</tspan>,", 1),
        ("available: <tspan fill='#FBBF24'>true</tspan>,", 1),
        ("};", 0),
    ]
    code_lines = "".join(
        f'<text class="mono" x="{776 + ind * 22}" y="{176 + i * 27}" font-size="15" fill="{TEXT}">{line}</text>'
        for i, (line, ind) in enumerate(code)
    )
    body = f"""
<rect width="{w}" height="{h}" rx="24" fill="{BG}"/>
<rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>
<g filter="url(#blur)" opacity="0.55">
  <circle cx="220" cy="120" r="150" fill="{VIOLET}">
    <animate attributeName="cx" values="220;330;220" dur="14s" repeatCount="indefinite"/>
    <animate attributeName="cy" values="120;200;120" dur="11s" repeatCount="indefinite"/>
  </circle>
  <circle cx="980" cy="330" r="160" fill="{CYAN}" fill-opacity="0.7">
    <animate attributeName="cx" values="980;860;980" dur="16s" repeatCount="indefinite"/>
  </circle>
  <circle cx="640" cy="420" r="120" fill="{PINK}" fill-opacity="0.6">
    <animate attributeName="cy" values="420;340;420" dur="12s" repeatCount="indefinite"/>
  </circle>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="24" stroke="{BORDER}"/>

<g class="fade" style="animation-delay:.1s">
  <rect x="64" y="64" width="290" height="34" rx="17" fill="{GREEN}" fill-opacity="0.10" stroke="{GREEN}" stroke-opacity="0.4"/>
  <circle cx="86" cy="81" r="5" fill="{GREEN}"/>
  <circle cx="86" cy="81" r="5" fill="{GREEN}" class="ping"/>
  <text class="mono" x="102" y="86" font-size="13" fill="{GREEN}" letter-spacing="1.5">AVAILABLE FOR NEW PROJECTS</text>
</g>
<g class="fade" style="animation-delay:.3s">
  <text x="62" y="172" font-size="60" font-weight="800" fill="url(#shine)" letter-spacing="-1.5">Md Tanvir Chowdhury</text>
</g>
<g class="fade" style="animation-delay:.5s">
  <text x="64" y="222" font-size="26" font-weight="600" fill="{TEXT}">Full-Stack &amp; AI Engineer</text>
</g>
<g class="fade" style="animation-delay:.7s">
  <text x="64" y="262" font-size="18" fill="{MUTED}">I turn ideas into fast, secure, AI-powered products</text>
  <text x="64" y="288" font-size="18" fill="{MUTED}">that real users love and businesses can grow on.</text>
</g>
<g class="fade" style="animation-delay:.9s">{pill_row(64, 326, tags, [PURPLE, CYAN, PINK])}</g>
<g class="fade" style="animation-delay:1.1s">
  <text class="mono" x="64" y="398" font-size="13" fill="{MUTED}">Dhaka, Bangladesh  ·  Remote, worldwide  ·  CSE @ North South University</text>
</g>

<g class="float">
  <rect x="748" y="96" width="388" height="262" rx="16" fill="#0E0E1A" fill-opacity="0.85" stroke="url(#brand)" stroke-opacity="0.6"/>
  <rect x="748" y="96" width="388" height="40" rx="16" fill="#ffffff" fill-opacity="0.03"/>
  <circle cx="772" cy="116" r="6" fill="#FF5F57"/><circle cx="792" cy="116" r="6" fill="#FEBC2E"/><circle cx="812" cy="116" r="6" fill="#28C840"/>
  <text class="mono" x="1112" y="121" text-anchor="end" font-size="12" fill="{MUTED}">tanvir.ts</text>
  {code_lines}
  <rect x="806" y="333" width="9" height="17" fill="{PURPLE}" class="blink"/>
</g>
"""
    defs = f"""
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="{PURPLE}"/>
    <stop offset="0.7" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>
  </linearGradient>"""
    style = """
  .fade { opacity: 0; animation: up .8s ease-out forwards; }
  @keyframes up { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
  .ping { transform-origin: 86px 81px; animation: ping 1.6s ease-out infinite; }
  @keyframes ping { from { transform: scale(1); opacity: .8; } to { transform: scale(2.8); opacity: 0; } }
  .float { animation: float 6s ease-in-out infinite; }
  @keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
  .blink { animation: blink 1s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }"""
    return svg(w, h, body, defs, style)


def section(num, title, subtitle):
    w, h = 1200, 92
    body = f"""
<text class="mono" x="2" y="34" font-size="14" fill="{PURPLE}" letter-spacing="3">{num} /</text>
<text x="0" y="72" font-size="34" font-weight="800" fill="{TEXT}" letter-spacing="-0.5">{escape(title)}</text>
<text x="1198" y="72" text-anchor="end" font-size="15" fill="{MUTED}">{escape(subtitle)}</text>
<rect x="0" y="88" width="{w}" height="1" fill="{BORDER}"/>
<rect x="0" y="87" width="160" height="3" rx="1.5" fill="url(#brand)">
  <animate attributeName="x" values="0;1040;0" dur="10s" repeatCount="indefinite"/>
</rect>
"""
    return svg(w, h, body)


def terminal():
    w = 1200
    rows = [
        ("whoami", [f"<tspan fill='{TEXT}'>Md Tanvir Chowdhury</tspan>  <tspan fill='{MUTED}'>·</tspan>  <tspan fill='{PURPLE}'>Full-Stack &amp; AI Engineer</tspan>"]),
        ("cat education.txt", [f"<tspan fill='{TEXT}'>B.Sc. Computer Science &amp; Engineering</tspan> <tspan fill='{MUTED}'>@ North South University</tspan>"]),
        ("ls ./expertise", [f"<tspan fill='{CYAN}'>backend-apis/   ai-rag-systems/   saas-platforms/   wordpress-plugins/   dev-tools/</tspan>"]),
        ("cat now.md", [f"<tspan fill='{TEXT}'>Building </tspan><tspan fill='{PINK}'>LucentEdit</tspan><tspan fill='{TEXT}'>, an open-source design editor with a built-in MCP server for AI agents</tspan>"]),
        ("echo $MOTTO", [f"<tspan fill='#86EFAC'>\"Clean code. Clear communication. Shipped on time.\"</tspan>"]),
    ]
    y = 96
    lines = []
    delay = 0.3
    for cmd, outs in rows:
        lines.append(
            f'<g class="ln" style="animation-delay:{delay:.1f}s"><text class="mono" x="40" y="{y}" font-size="16">'
            f"<tspan fill='{GREEN}'>tanvir@dev</tspan><tspan fill='{MUTED}'>:</tspan><tspan fill='{CYAN}'>~</tspan>"
            f"<tspan fill='{MUTED}'>$ </tspan><tspan fill='{TEXT}'>{escape(cmd)}</tspan></text></g>"
        )
        y += 28
        delay += 0.45
        for out in outs:
            lines.append(f'<g class="ln" style="animation-delay:{delay:.1f}s"><text class="mono" x="40" y="{y}" font-size="16">{out}</text></g>')
            y += 40
            delay += 0.35
    lines.append(
        f'<g class="ln" style="animation-delay:{delay:.1f}s"><text class="mono" x="40" y="{y}" font-size="16">'
        f"<tspan fill='{GREEN}'>tanvir@dev</tspan><tspan fill='{MUTED}'>:</tspan><tspan fill='{CYAN}'>~</tspan><tspan fill='{MUTED}'>$ </tspan></text>"
        f'<rect x="168" y="{y - 14}" width="9" height="18" fill="{PURPLE}" class="blink"/></g>'
    )
    h = y + 36
    body = f"""
<rect width="{w}" height="{h}" rx="18" fill="{BG}"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#grid)"/>
<circle cx="1100" cy="{h}" r="140" fill="{VIOLET}" opacity="0.25" filter="url(#blur)"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" stroke="{BORDER}"/>
<path d="M0 18a18 18 0 0 1 18-18h{w - 36}a18 18 0 0 1 18 18v28H0z" fill="#ffffff" fill-opacity="0.03"/>
<circle cx="28" cy="23" r="7" fill="#FF5F57"/><circle cx="52" cy="23" r="7" fill="#FEBC2E"/><circle cx="76" cy="23" r="7" fill="#28C840"/>
<text class="mono" x="{w / 2}" y="28" text-anchor="middle" font-size="13" fill="{MUTED}">tanvir@dev: ~  —  zsh</text>
{''.join(lines)}
"""
    style = """
  .ln { opacity: 0; animation: show .35s ease-out forwards; }
  @keyframes show { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: none; } }
  .blink { animation: blink 1s steps(1) infinite; }
  @keyframes blink { 50% { opacity: 0; } }"""
    return svg(w, h, body, style=style)


def icon(kind, cx, cy, color):
    """Small line-art glyphs drawn with paths so they render identically everywhere."""
    s = f'stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"'
    if kind == "ai":
        return (f'<g {s}><rect x="{cx-14}" y="{cy-14}" width="28" height="28" rx="6"/>'
                f'<path d="M{cx-6} {cy-20}v6M{cx+6} {cy-20}v6M{cx-6} {cy+14}v6M{cx+6} {cy+14}v6'
                f'M{cx-20} {cy-6}h6M{cx-20} {cy+6}h6M{cx+14} {cy-6}h6M{cx+14} {cy+6}h6"/>'
                f'<circle cx="{cx}" cy="{cy}" r="5"/></g>')
    if kind == "api":
        return (f'<g {s}><ellipse cx="{cx}" cy="{cy-11}" rx="15" ry="6"/>'
                f'<path d="M{cx-15} {cy-11}v22c0 3.3 6.7 6 15 6s15-2.7 15-6v-22M{cx-15} {cy}c0 3.3 6.7 6 15 6s15-2.7 15-6"/></g>')
    if kind == "saas":
        return (f'<g {s}><rect x="{cx-18}" y="{cy-14}" width="36" height="26" rx="4"/>'
                f'<path d="M{cx-8} {cy+18}h16M{cx} {cy+12}v6M{cx-10} {cy+4}l6-8 5 5 8-9"/></g>')
    return (f'<g {s}><path d="M{cx-4} {cy-18}l-4 8h8l-4 8M{cx+2} {cy}"/>'
            f'<path d="M{cx-18} {cy+4}l8-8M{cx-18} {cy+4}l8 8M{cx+18} {cy+4}l-8-8M{cx+18} {cy+4}l-8 8"/></g>')


def services():
    w, h = 1200, 560
    items = [
        ("ai", "AI & LLM Solutions", VIOLET,
         ["RAG chatbots trained on your own documents",
          "LLM assistants for web, Telegram and APIs",
          "MCP servers so AI agents can use your product"],
         ["LLMs", "RAG", "Pinecone", "MCP"]),
        ("api", "Backend & APIs", CYAN,
         ["Secure, documented REST APIs that scale",
          "Auth, payments, background jobs, integrations",
          "Clean data models on SQL and NoSQL"],
         ["Django", "DRF", "FastAPI", "PostgreSQL"]),
        ("saas", "SaaS & Web Apps", PINK,
         ["End-to-end products from idea to launch",
          "Dashboards, role-based portals, subscriptions",
          "Fast, responsive, polished user interfaces"],
         ["React", "Vue", "Tailwind", "Vercel"]),
        ("auto", "Plugins & Automation", GREEN,
         ["Custom WordPress plugins for your store",
          "Bots, scrapers and workflow automation",
          "Scripts that save your team hours every week"],
         ["WordPress", "PHP", "Python", "Bots"]),
    ]
    cw, ch, gap = 588, 268, 24
    cards = []
    for i, (kind, title, color, bullets, tags) in enumerate(items):
        x = (i % 2) * (cw + gap)
        y = (i // 2) * (ch + gap)
        bl = "".join(
            f'<circle cx="{x + 36}" cy="{y + 132 + j * 30}" r="3" fill="{color}"/>'
            f'<text x="{x + 50}" y="{y + 137 + j * 30}" font-size="16" fill="{MUTED}">{escape(b)}</text>'
            for j, b in enumerate(bullets)
        )
        cards.append(f"""
<g class="card" style="animation-delay:{0.15 * i:.2f}s">
  <rect x="{x + 0.5}" y="{y + 0.5}" width="{cw - 1}" height="{ch - 1}" rx="18" fill="url(#cardbg)" stroke="{BORDER}"/>
  <circle cx="{x + cw - 40}" cy="{y + 30}" r="70" fill="{color}" opacity="0.18" filter="url(#soft)"/>
  <rect x="{x + 28}" y="{y}" width="120" height="3" rx="1.5" fill="{color}"/>
  <rect x="{x + 28}" y="{y + 28}" width="56" height="56" rx="14" fill="{color}" fill-opacity="0.12" stroke="{color}" stroke-opacity="0.4"/>
  {icon(kind, x + 56, y + 56, color)}
  <text x="{x + 104}" y="{y + 64}" font-size="24" font-weight="700" fill="{TEXT}">{escape(title)}</text>
  {bl}
  {pill_row(x + 28, y + 222, tags, [color], size=12)}
</g>""")
    style = """
  .card { opacity: 0; animation: up .7s ease-out forwards; }
  @keyframes up { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }"""
    return svg(w, h, "".join(cards), style=style)


def process():
    w, h = 1200, 200
    steps = [
        ("01", "Discover", "Goals, users, scope"),
        ("02", "Plan", "Architecture & timeline"),
        ("03", "Build", "Weekly demos & updates"),
        ("04", "Launch", "Tested, deployed, live"),
        ("05", "Support", "Docs, handover, care"),
    ]
    colors = [VIOLET, PURPLE, PINK, CYAN, GREEN]
    xs = [120 + i * 240 for i in range(5)]
    nodes = []
    for i, ((n, t, s), x) in enumerate(zip(steps, xs)):
        c = colors[i]
        nodes.append(f"""
<g class="step" style="animation-delay:{0.2 * i:.1f}s">
  <circle cx="{x}" cy="62" r="34" fill="{BG}" stroke="{c}" stroke-width="2"/>
  <circle cx="{x}" cy="62" r="34" fill="{c}" fill-opacity="0.12"/>
  <text class="mono" x="{x}" y="69" text-anchor="middle" font-size="20" font-weight="700" fill="{c}">{n}</text>
  <text x="{x}" y="134" text-anchor="middle" font-size="20" font-weight="700" fill="{TEXT}">{t}</text>
  <text x="{x}" y="162" text-anchor="middle" font-size="14" fill="{MUTED}">{escape(s)}</text>
</g>""")
    body = f"""
<path d="M{xs[0]} 62H{xs[-1]}" stroke="{BORDER}" stroke-width="2"/>
<path d="M{xs[0]} 62H{xs[-1]}" stroke="url(#brand)" stroke-width="2" stroke-dasharray="8 10">
  <animate attributeName="stroke-dashoffset" values="0;-180" dur="4s" repeatCount="indefinite"/>
</path>
{''.join(nodes)}
"""
    style = """
  .step { opacity: 0; animation: up .6s ease-out forwards; }
  @keyframes up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }"""
    return svg(w, h, body, style=style)


def project(name, kind, desc, tags, color, featured=False):
    w = 1200 if featured else 590
    chars = 110 if featured else 58
    lines = wrap(desc, chars)
    # Grid cards share one height so rows line up in the README.
    assert featured or len(lines) <= 3, f"{name}: description too long"
    h = 150 + (len(lines) if featured else 3) * 26 + 50
    text = "".join(
        f'<text x="32" y="{132 + i * 26}" font-size="16" fill="{MUTED}">{escape(l)}</text>' for i, l in enumerate(lines)
    )
    badge = ""
    if featured:
        m, _ = pill(w - 190, 30, "★ FEATURED", "#FBBF24", 12)
        badge = m
    # "StreamFlex" -> "SF", "WebShield AI" -> "WA": split on spaces and CamelCase humps.
    words = re.findall(r"[A-Z][a-z]*|[a-z]+", name)
    initials = "".join(w[0] for w in words[:2]).upper()
    body = f"""
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="url(#cardbg)" stroke="{BORDER}"/>
<circle cx="{w - 60}" cy="{h}" r="110" fill="{color}" opacity="0.22" filter="url(#soft)"/>
<rect x="0" y="0" width="{w}" height="3" rx="1.5" fill="{color}" opacity="0.9"/>
<rect x="32" y="30" width="52" height="52" rx="14" fill="{color}" fill-opacity="0.14" stroke="{color}" stroke-opacity="0.45"/>
<text x="58" y="63" text-anchor="middle" font-size="19" font-weight="800" fill="{color}">{escape(initials)}</text>
<text x="100" y="54" font-size="{28 if featured else 24}" font-weight="800" fill="{TEXT}">{escape(name)}</text>
<text class="mono" x="101" y="77" font-size="12" fill="{color}" letter-spacing="1.5">{escape(kind.upper())}</text>
{badge}
<rect x="32" y="102" width="{w - 64}" height="1" fill="{BORDER}"/>
{text}
{pill_row(32, h - 52, tags, [color], size=12)}
<text x="{w - 32}" y="{h - 33}" text-anchor="end" font-size="14" font-weight="600" fill="{TEXT}" class="arrow">View project  →</text>
"""
    style = ".arrow { animation: nudge 2.4s ease-in-out infinite; } @keyframes nudge { 0%,100% { transform: none; } 50% { transform: translateX(4px); } }"
    return svg(w, h, body, style=style)


def cta():
    w, h = 1200, 260
    body = f"""
<rect width="{w}" height="{h}" rx="24" fill="{BG}"/>
<rect width="{w}" height="{h}" rx="24" fill="url(#grid)"/>
<g filter="url(#blur)" opacity="0.5">
  <circle cx="300" cy="260" r="140" fill="{VIOLET}"><animate attributeName="cx" values="300;500;300" dur="12s" repeatCount="indefinite"/></circle>
  <circle cx="900" cy="0" r="140" fill="{CYAN}"><animate attributeName="cx" values="900;700;900" dur="12s" repeatCount="indefinite"/></circle>
</g>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="24" stroke="url(#brand)" stroke-opacity="0.6"/>
<text x="{w / 2}" y="92" text-anchor="middle" font-size="40" font-weight="800" fill="{TEXT}" letter-spacing="-0.5">Have a project in mind?</text>
<text x="{w / 2}" y="132" text-anchor="middle" font-size="18" fill="{MUTED}">Freelance, contract or full-time. Let's turn your idea into a product people love.</text>
<g class="pulse">
  <rect x="{w / 2 - 130}" y="164" width="260" height="54" rx="27" fill="url(#brand)"/>
  <text x="{w / 2}" y="198" text-anchor="middle" font-size="18" font-weight="700" fill="#ffffff">Start a conversation  →</text>
</g>
"""
    style = ".pulse { transform-origin: 600px 191px; animation: pulse 2.6s ease-in-out infinite; } @keyframes pulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.04); } }"
    return svg(w, h, body, style=style)


def timeline_css(selector_steps, cycle):
    """Per-element keyframes so each element appears at its own moment and the whole scene loops."""
    css = []
    for i, start in enumerate(selector_steps):
        on = start / cycle * 100
        css.append(
            f".s{i} {{ animation: k{i} {cycle}s linear infinite; }}"
            f"@keyframes k{i} {{ 0%, {on:.2f}% {{ opacity: 0; }} {on + 2:.2f}%, 94% {{ opacity: 1; }} 98%, 100% {{ opacity: 0; }} }}"
        )
    return "\n".join(css)


def lucent_demo():
    """Looping demo: an AI agent drives LucentEdit through its real MCP tools and the canvas fills in."""
    w, h, cycle = 1200, 470, 14
    prompt = "Design a 1280x640 launch card for my coffee shop, preview it, then export a PNG."
    calls = [
        ("new_document", "{ width: 1280, height: 640 }"),
        ("add_shape", "{ shape: 'rect', fill: gradient }"),
        ("add_text", "{ text: 'Brew Day', font_size: 96 }"),
        ("add_shape", "{ shape: 'star', points: 8 }"),
        ("update_layer", "{ effects: { glow } }"),
        ("render_preview", "{ }  → looks great"),
        ("export_document", "{ format: 'png' }"),
    ]
    starts = [0.4, 1.4]  # prompt, "thinking"
    starts += [2.4 + i * 1.2 for i in range(len(calls))]
    rows = []
    rows.append(
        f'<g class="s0"><rect x="40" y="96" width="500" height="64" rx="12" fill="{VIOLET}" fill-opacity="0.14" stroke="{VIOLET}" stroke-opacity="0.35"/>'
        + "".join(
            f'<text x="56" y="{122 + i * 22}" font-size="14" fill="{TEXT}">{escape(l)}</text>'
            for i, l in enumerate(wrap(prompt, 62))
        )
        + "</g>"
    )
    rows.append(f'<g class="s1"><text class="mono" x="40" y="190" font-size="13" fill="{MUTED}">✻ Calling LucentEdit over MCP…</text></g>')
    for i, (tool, args) in enumerate(calls):
        y = 222 + i * 32
        rows.append(
            f'<g class="s{i + 2}"><text class="mono" x="40" y="{y}" font-size="14">'
            f"<tspan fill='{GREEN}'>✓</tspan> <tspan fill='{CYAN}'>{tool}</tspan>"
            f"<tspan fill='{MUTED}'> {escape(args)}</tspan></text></g>"
        )
    # Canvas elements keyed to the tool call that creates them.
    cx, cy, cw, ch = 640, 120, 520, 260
    c = lambda n: f"s{n + 2}"
    canvas = f"""
<g class="{c(0)}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="#ffffff" fill-opacity="0.04" stroke="{BORDER}"/></g>
<g class="{c(1)}"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="url(#coffee)"/></g>
<g class="{c(2)}">
  <text x="{cx + 36}" y="{cy + 130}" font-size="54" font-weight="800" fill="#FFF7ED">Brew Day</text>
  <text x="{cx + 38}" y="{cy + 166}" font-size="16" fill="#FED7AA">Grand opening · Saturday 9 AM</text>
</g>
<g class="{c(3)}"><path d="{star_path(cx + 410, cy + 120, 62, 30, 8)}" fill="#FDBA74"/></g>
<g class="{c(4)}"><path d="{star_path(cx + 410, cy + 120, 62, 30, 8)}" fill="#FDBA74" filter="url(#glowf)" opacity="0.9"/></g>
<g class="{c(5)}"><rect x="{cx - 4}" y="{cy - 4}" width="{cw + 8}" height="{ch + 8}" rx="4" stroke="{CYAN}" stroke-dasharray="6 6"/>
  <text class="mono" x="{cx + cw}" y="{cy - 12}" text-anchor="end" font-size="12" fill="{CYAN}">render_preview.png</text></g>
<g class="{c(6)}"><rect x="{cx + cw - 170}" y="{cy + ch + 18}" width="170" height="34" rx="17" fill="{GREEN}" fill-opacity="0.15" stroke="{GREEN}" stroke-opacity="0.5"/>
  <text class="mono" x="{cx + cw - 85}" y="{cy + ch + 40}" text-anchor="middle" font-size="13" fill="{GREEN}">✓ exported .png</text></g>
"""
    layers = ["Background", "Gradient", "Brew Day", "Star", "Glow"]
    layer_rows = "".join(
        f'<g class="{c(min(i, 4))}"><rect x="{cx - 128}" y="{cy + 26 + i * 30}" width="112" height="24" rx="5" fill="#ffffff" fill-opacity="0.04"/>'
        f'<text x="{cx - 120}" y="{cy + 42 + i * 30}" font-size="12" fill="{MUTED}">▢ {name}</text></g>'
        for i, name in enumerate(layers)
    )
    body = f"""
<rect width="{w}" height="{h}" rx="20" fill="{BG}"/>
<rect width="{w}" height="{h}" rx="20" fill="url(#grid)"/>
<circle cx="900" cy="250" r="180" fill="{PINK}" opacity="0.18" filter="url(#blur)"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="20" stroke="{BORDER}"/>
<text class="mono" x="40" y="58" font-size="13" fill="{PURPLE}" letter-spacing="2">AI AGENT</text>
<text x="40" y="80" font-size="13" fill="{MUTED}">Claude Code · Cursor · Copilot · Codex · Gemini</text>
<text class="mono" x="{cx - 128}" y="58" font-size="13" fill="{PINK}" letter-spacing="2">LUCENTEDIT</text>
<text x="{cx - 128}" y="80" font-size="13" fill="{MUTED}">built-in MCP server · 127.0.0.1:47800/mcp</text>
<text class="mono" x="{cx - 128}" y="{cy + 12}" font-size="11" fill="{MUTED}" letter-spacing="1.5">LAYERS</text>
<line x1="{cx - 150}" y1="96" x2="{cx - 150}" y2="{h - 40}" stroke="{BORDER}"/>
{''.join(rows)}
{layer_rows}
{canvas}
"""
    defs = f"""
  <linearGradient id="coffee" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7C2D12"/><stop offset="0.6" stop-color="#C2410C"/><stop offset="1" stop-color="#F59E0B"/>
  </linearGradient>
  <filter id="glowf" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>"""
    return svg(w, h, body, defs, timeline_css(starts, cycle))


def star_path(cx, cy, r_out, r_in, points):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


TESTIMONIALS = [
    ("Tanvir has done a great job with our marketing and has played a big part in "
     "bringing in more sales for us.",
     "CEO", "Phoenix Education & Automata One", VIOLET),
    ("Tanvir really knows his craft. He built great websites for me, and for my "
     "friends too.",
     "Rahat Hassan", "Client", CYAN),
    ("Tanvir built a great website for me last time. That's exactly why I came back "
     "to him for my next project.",
     "Ahein", "Returning client", PINK),
]


def testimonials():
    w, h = 1200, 280
    cw, gap = 384, 24
    cards = []
    for i, (quote, name, role, color) in enumerate(TESTIMONIALS):
        x = i * (cw + gap)
        lines = wrap(quote, 34)
        q = "".join(
            f'<text x="{x + 32}" y="{y}" font-size="18" fill="{TEXT}">{escape(l)}</text>'
            for l, y in zip(lines, range(100, 400, 30))
        )
        initials = "".join(p[0] for p in name.split()[:2]).upper()
        cards.append(f"""
<g class="card" style="animation-delay:{0.2 * i:.1f}s">
  <rect x="{x + 0.5}" y="0.5" width="{cw - 1}" height="{h - 1}" rx="18" fill="url(#cardbg)" stroke="{BORDER}"/>
  <circle cx="{x + cw - 30}" cy="20" r="80" fill="{color}" opacity="0.16" filter="url(#soft)"/>
  <rect x="{x + 32}" y="0" width="80" height="3" rx="1.5" fill="{color}"/>
  <text x="{x + 28}" y="74" font-size="64" font-weight="800" fill="{color}" opacity="0.55" font-family="Georgia, serif">“</text>
  {q}
  <rect x="{x + 32}" y="{h - 92}" width="{cw - 64}" height="1" fill="{BORDER}"/>
  <circle cx="{x + 56}" cy="{h - 48}" r="22" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-opacity="0.5"/>
  <text x="{x + 56}" y="{h - 42}" text-anchor="middle" font-size="15" font-weight="700" fill="{color}">{escape(initials)}</text>
  <text x="{x + 90}" y="{h - 53}" font-size="16" font-weight="700" fill="{TEXT}">{escape(name)}</text>
  <text x="{x + 90}" y="{h - 32}" font-size="13" fill="{MUTED}">{escape(role)}</text>
</g>""")
    style = """
  .card { opacity: 0; animation: up .7s ease-out forwards; }
  @keyframes up { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }"""
    return svg(w, h, "".join(cards), style=style)


PROJECTS = {
    "lucentedit": ("LucentEdit", "Open-source desktop app · AI-native",
                   "A free, lightweight, open-source Photoshop + Illustrator alternative. Layers, pen paths, filters and "
                   "PSD import/export in a tiny cross-platform binary, plus a built-in MCP server so Claude, Cursor, "
                   "Copilot, Codex and Gemini can design for you. No signup, no subscription.",
                   ["MCP", "AI Agents", "macOS", "Windows", "Linux", "MIT"], PINK, True),
    "webshield": ("WebShield AI", "Security SaaS",
                  "AI-powered web intrusion detection and auto-defense. A lightweight JS agent streams traffic to an ML "
                  "backend for real-time threat detection and visual dashboards.",
                  ["Vue", "FastAPI", "PostgreSQL", "ML"], CYAN, False),
    "chatbot": ("RAG AI Chatbot", "AI backend",
                "Production-style RAG chatbot API with Pinecone vector search, Mistral AI generation, JWT auth, email "
                "verification, chat history and scheduled background jobs.",
                ["Django REST", "RAG", "Pinecone", "Mistral"], VIOLET, False),
    "phoenix": ("Phoenix Bot", "Client project · EdTech",
                "A 24/7 AI tutor for an admission coaching business. Answers Math, English and Analytical "
                "questions, even from photos, right inside Telegram.",
                ["Python", "LLM", "Telegram", "Vision"], "#FB923C", False),
    "bizconnect": ("BizConnect", "Platform · Startups",
                   "All-in-one platform connecting entrepreneurs, investors and students with role-based portals, "
                   "networking, recruitment and Firebase authentication.",
                   ["React", "Tailwind", "Firebase", "Framer"], PURPLE, False),
    "phoneguard": ("BD Phone Guard", "WordPress plugin · E-commerce",
                   "Validates and normalizes Bangladeshi phone numbers, including Bangla digits and pasted junk, so "
                   "cash-on-delivery stores get clean numbers for couriers and SMS.",
                   ["PHP", "WordPress", "E-commerce"], GREEN, False),
    "streamflex": ("StreamFlex", "Streaming platform",
                   "Full movie streaming platform with subscriptions, payments, cart, user dashboards and a powerful "
                   "admin panel for managing the catalogue.",
                   ["PHP", "MySQL", "Payments"], "#F87171", False),
    "datalens": ("DataLens", "Data analytics · Desktop",
                 "C++ and Qt6 analytics app on the Olympic 2024 dataset, powered by a custom-built database engine, "
                 "graph algorithms and statistical charts.",
                 ["C++", "Qt6", "Data Structures"], "#60A5FA", False),
    "more": ("And much more", "Portfolio · 50+ repositories",
             "Short-video platforms, Django backends, ML notebooks, games and tools. Explore everything on my "
             "portfolio and repositories.",
             ["Portfolio", "Open Source"], "#FBBF24", False),
}

SECTIONS = {
    "about": ("01", "About Me", "who I am & what drives me"),
    "services": ("02", "What I Build For You", "services for clients & teams"),
    "process": ("03", "How We'll Work", "a simple, transparent process"),
    "projects": ("04", "Featured Work", "products I've designed & shipped"),
    "testimonials": ("05", "What Clients Say", "kind words from people I've built for"),
    "stack": ("06", "Tech Stack", "tools I use to ship"),
    "stats": ("07", "Activity & Analytics", "consistency, in numbers"),
    "contact": ("08", "Let's Connect", "open to freelance & full-time roles"),
}


def main():
    files = {
        "hero.svg": hero(),
        "terminal.svg": terminal(),
        "services.svg": services(),
        "process.svg": process(),
        "cta.svg": cta(),
        "lucentedit-demo.svg": lucent_demo(),
        "testimonials.svg": testimonials(),
    }
    for key, args in SECTIONS.items():
        files[f"section-{key}.svg"] = section(*args)
    for key, args in PROJECTS.items():
        files[f"project-{key}.svg"] = project(*args)
    for name, content in files.items():
        (OUT / name).write_text(content)
    print(f"wrote {len(files)} files to {OUT}")


if __name__ == "__main__":
    main()
