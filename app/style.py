"""Styling helpers for the Exoplanet Explorer dashboard (colors, CSS and small HTML pieces)."""
import streamlit as st

# Color palette (matches the approved mockup, Option C)
BG = "#15202B"
CARD = "#192734"
BORDER = "#2E3D4B"
GRID = "#22303C"
TEXT = "#F5F8FA"
SOFT = "#C3CED8"
MUTED = "#8899A6"
MINT = "#8FD9A8"
CYAN = "#7CC4E4"
AMBER = "#F2C14E"
LILAC = "#B9A6F5"
CORAL = "#F08A7E"
SLATE = "#6E8091"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600&family=Inter:wght@400;500;600&display=swap');

html, body, .stApp { font-family: 'Inter', sans-serif; }
h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; }
.block-container { padding-top: 2rem; max-width: 1200px; }

/* Sidebar */
[data-testid="stSidebar"] { border-right: 1px solid #22303C; }

/* Multiselect chips: soft, small, readable */
[data-testid="stMultiSelect"] [data-baseweb="tag"] { background-color: rgba(143,217,168,0.14) !important; border: 1px solid rgba(143,217,168,0.4) !important; border-radius: 999px !important; height: 26px !important; margin: 3px !important; }
[data-testid="stMultiSelect"] [data-baseweb="tag"] * { color: #D9F2E1 !important; font-size: 12px !important; }

/* Tabs as a pill menu */
.stTabs [role="tablist"] { gap: 4px; padding: 5px; background: #192734; border: 1px solid #2E3D4B !important; border-radius: 999px; width: fit-content; margin: 0 auto 1.5rem auto; box-shadow: none !important; }
.stTabs [role="tab"] { height: 38px; padding: 0 18px !important; border-radius: 999px !important; background: transparent; border: none !important; box-shadow: none !important; }
.stTabs [role="tab"] p { color: #C3CED8; font-weight: 500; }
.stTabs [role="tab"][aria-selected="true"] { background: #F5F8FA !important; }
.stTabs [role="tab"][aria-selected="true"] p { color: #15202B !important; }
.stTabs [role="tab"]::after, .stTabs [role="tablist"]::after, .stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs .react-aria-SelectionIndicator { left: 25% !important; right: 25% !important; width: auto !important; border-radius: 999px !important; }

/* Cards made with st.container(border=True, key="card_...") */
[class*="st-key-card"] { background: #192734; border: 1px solid #2E3D4B !important; border-radius: 20px !important; padding: 22px 24px !important; }

/* Small building blocks */
.label { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; color: #8899A6; text-transform: uppercase; }
.pill { display: inline-block; font-size: 10px; font-weight: 600; letter-spacing: 0.1em; padding: 3px 10px; border-radius: 999px; white-space: nowrap; }
.pill-good { color: #8FD9A8; border: 1px solid rgba(143,217,168,0.45); }
.pill-warn { color: #F2C14E; border: 1px solid rgba(242,193,78,0.5); }
.pill-info { color: #7CC4E4; border: 1px solid rgba(124,196,228,0.45); }
.card-head { display: flex; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 4px; }
.card-title { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 500; color: #F5F8FA; margin: 2px 0 0 0; }

.insight { display: flex; gap: 12px; align-items: flex-start; padding: 14px 16px; border-radius: 12px; background: #15202B; border: 1px solid #22303C; color: #C3CED8; font-size: 14px; margin-top: 8px; }
.insight b { font-size: 11px; letter-spacing: 0.14em; color: #8FD9A8; margin-right: 6px; }
.note { background: rgba(242,193,78,0.08); border: 1px solid rgba(242,193,78,0.35); color: #E9DDBF; }
.note b { color: #F2C14E; }

.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 4px 0 20px 0; }
.stat { display: flex; flex-direction: column; gap: 6px; padding: 18px 20px; border: 1px solid #2E3D4B; border-radius: 16px; background: #192734; }
.stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 38px; font-weight: 300; line-height: 1.1; color: #F5F8FA; }
.stat-sub { font-size: 13px; color: #8899A6; }

.ring { position: relative; width: 64px; height: 64px; flex: none; border-radius: 50%; }
.ring span { position: absolute; inset: 6px; border-radius: 50%; background: #192734; display: flex; align-items: center; justify-content: center; font-family: 'Space Grotesk', sans-serif; font-size: 14px; color: #F5F8FA; }

/* Hero */
.hero { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; align-items: center; padding: 36px 40px; border: 1px solid #2E3D4B; border-radius: 24px; background: #192734; margin-bottom: 20px; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-weight: 300; font-size: clamp(30px, 3.6vw, 48px); line-height: 1.06; letter-spacing: -0.01em; margin: 18px 0 14px 0; color: #F5F8FA; }
.hero-title span { color: #8FD9A8; }
.hero p { color: #C3CED8; font-size: 16px; max-width: 440px; margin: 0; }
.hero-art { position: relative; height: 300px; }
.target { position: absolute; right: 0; top: 14px; display: flex; flex-direction: column; gap: 2px; padding: 12px 16px; border: 1px solid #3A4B5B; border-radius: 14px; background: rgba(21,32,43,0.85); }
.target strong { font-family: 'Space Grotesk', sans-serif; font-size: 18px; font-weight: 500; color: #F5F8FA; }

/* Starfield background (behind all cards) */
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stAppViewContainer"] {
  background-color: #15202B !important;
  background-image:
    radial-gradient(1px 1px at 40px 60px, rgba(255,255,255,0.70) 50%, transparent 52%),
    radial-gradient(1px 1px at 130px 210px, rgba(255,255,255,0.50) 50%, transparent 52%),
    radial-gradient(1.5px 1.5px at 300px 80px, rgba(255,255,255,0.80) 50%, transparent 52%),
    radial-gradient(1px 1px at 420px 330px, rgba(255,255,255,0.60) 50%, transparent 52%),
    radial-gradient(1px 1px at 210px 460px, rgba(255,255,255,0.45) 50%, transparent 52%),
    radial-gradient(1.5px 1.5px at 480px 150px, rgba(143,217,168,0.60) 50%, transparent 52%),
    radial-gradient(1px 1px at 90px 380px, rgba(124,196,228,0.55) 50%, transparent 52%),
    radial-gradient(2px 2px at 150px 120px, rgba(255,255,255,0.45) 50%, transparent 52%),
    radial-gradient(1.5px 1.5px at 620px 300px, rgba(255,255,255,0.60) 50%, transparent 52%),
    radial-gradient(2px 2px at 400px 700px, rgba(185,166,245,0.45) 50%, transparent 52%),
    radial-gradient(1px 1px at 760px 560px, rgba(255,255,255,0.50) 50%, transparent 52%) !important;
  background-size:
    520px 520px, 520px 520px, 520px 520px, 520px 520px, 520px 520px, 520px 520px, 520px 520px,
    830px 830px, 830px 830px, 830px 830px, 830px 830px !important;
}

/* Shooting stars */
.sky { position: fixed; inset: 0; pointer-events: none; overflow: hidden; z-index: 0; }
.shoot { position: absolute; width: 140px; height: 1px; opacity: 0;
         background: linear-gradient(90deg, rgba(255,255,255,0.9), rgba(255,255,255,0));
         animation: shoot 10s linear infinite; }
.shoot.s1 { top: 14%; left: 6%;  animation-delay: 1s; }
.shoot.s2 { top: 58%; left: 90%; animation-delay: 4.5s; animation-duration: 12s; }
.shoot.s3 { top: 32%; left: 93%; animation-delay: 8s;   animation-duration: 14s; }
@keyframes shoot {
  0%   { opacity: 0; transform: rotate(-35deg) translateX(0); }
  2%   { opacity: 1; }
  9%   { opacity: 0; transform: rotate(-35deg) translateX(-280px); }
  100% { opacity: 0; transform: rotate(-35deg) translateX(-280px); }
}
@media (prefers-reduced-motion: reduce) { .shoot { display: none; } }
</style>
"""


def html(markup):
    """Show custom HTML. Lines are joined so Markdown doesn't turn indented lines into code blocks."""
    st.markdown(" ".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


def apply_style():
    html(CSS)


def card_header(label, title, pill=None, kind="good"):
    pill_html = f'<span class="pill pill-{kind}">{pill}</span>' if pill else ""
    html(f"""
    <div class="card-head">
      <div><div class="label">{label}</div><div class="card-title">{title}</div></div>
      {pill_html}
    </div>
    """)


def insight(text, title="INSIGHT", note=False):
    extra = " note" if note else ""
    html(f'<div class="insight{extra}"><div><b>{title}</b>{text}</div></div>')


def stat_cards(cards):
    """cards: list of dicts with label, value, sub, pill, kind."""
    items = ""
    for c in cards:
        items += f"""
        <div class="stat">
          <div class="card-head"><span class="label">{c['label']}</span><span class="pill pill-{c['kind']}">{c['pill']}</span></div>
          <div class="stat-value">{c['value']}</div>
          <div class="stat-sub">{c['sub']}</div>
        </div>
        """
    html(f'<div class="grid">{items}</div>')


def gauge_cards(gauges):
    """gauges: list of dicts with label, pct, value, sub, color, pill, kind."""
    items = ""
    for g in gauges:
        ring = f"background: conic-gradient({g['color']} 0 {g['pct']}%, {BORDER} {g['pct']}% 100%);"
        items += f"""
        <div class="stat">
          <div class="card-head"><span class="label">{g['label']}</span><span class="pill pill-{g['kind']}">{g['pill']}</span></div>
          <div style="display:flex; align-items:center; gap:16px;">
            <div class="ring" style="{ring}"><span>{g['pct']}%</span></div>
            <div style="display:flex; flex-direction:column;">
              <span style="font-family:'Space Grotesk',sans-serif; font-size:20px;">{g['value']}</span>
              <span class="stat-sub">{g['sub']}</span>
            </div>
          </div>
        </div>
        """
    html(f'<div class="grid">{items}</div>')


PLANET_SVG = """
<svg viewBox="0 0 420 320" width="100%" height="100%" role="img" aria-label="Illustration of a planet with an orbit and two moons">
  <defs>
    <radialGradient id="planet" cx="35%" cy="32%" r="75%"><stop offset="0%" stop-color="#7FB89A"/><stop offset="38%" stop-color="#3E6E73"/><stop offset="72%" stop-color="#1D3346"/><stop offset="100%" stop-color="#121B26"/></radialGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="60%" stop-color="#8FD9A8" stop-opacity="0.16"/><stop offset="100%" stop-color="#8FD9A8" stop-opacity="0"/></radialGradient>
    <radialGradient id="moon" cx="35%" cy="30%" r="80%"><stop offset="0%" stop-color="#9AA8B5"/><stop offset="100%" stop-color="#26323E"/></radialGradient>
  </defs>
  <circle cx="40" cy="40" r="1.2" fill="#C3CED8"/><circle cx="380" cy="30" r="1" fill="#C3CED8"/><circle cx="300" cy="290" r="1.4" fill="#C3CED8"/><circle cx="70" cy="260" r="1" fill="#C3CED8"/><circle cx="150" cy="20" r="0.9" fill="#C3CED8"/>
  <circle cx="240" cy="160" r="150" fill="url(#glow)"/>
  <ellipse cx="240" cy="165" rx="190" ry="58" fill="none" stroke="#8899A6" stroke-opacity="0.35" transform="rotate(-18 240 165)"/>
  <circle cx="240" cy="160" r="112" fill="url(#planet)"/>
  <path d="M150 120c30 8 50-6 80 2s44 22 76 12M140 175c26-6 48 10 78 4s52-20 86-6M170 228c22-8 40 2 64-2s34-12 54-4" fill="none" stroke="#9FD4B4" stroke-opacity="0.18" stroke-width="7" stroke-linecap="round"/>
  <circle cx="92" cy="210" r="16" fill="url(#moon)"/><circle cx="372" cy="96" r="9" fill="url(#moon)"/><circle cx="300" cy="234" r="3" fill="#F5F8FA"/>
</svg>
"""


def hero(n_planets, nearest_name, nearest_ly):
    html(f"""
    <div class="hero">
      <div>
        <span class="pill pill-good">NASA EXOPLANET ARCHIVE · {n_planets:,} PLANETS</span>
        <div class="hero-title">HOW CLOSE ARE WE<br>TO FINDING<br><span>ANOTHER EARTH?</span></div>
        <p>Explore every confirmed exoplanet: what kinds of worlds exist, how we found them, and which ones might be like home.</p>
      </div>
      <div class="hero-art">
        {PLANET_SVG}
        <div class="target">
          <span class="label">Nearest candidate</span>
          <strong>{nearest_name}</strong>
          <span class="label">Distance {nearest_ly:.1f} ly</span>
        </div>
      </div>
    </div>
    """)


def style_chart(fig, height=360, left=70, bottom=60):
    """Give every Plotly chart the same dim-space look."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=SOFT, size=12),
        margin=dict(l=left, r=20, t=30, b=bottom),
        legend=dict(orientation="h", y=1.1, x=0, title=None, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=CARD, bordercolor=BORDER, font_color=TEXT),
    )
    axis_style = dict(
        gridcolor=GRID, zerolinecolor=GRID, linecolor=BORDER, automargin=True,
        tickfont=dict(size=11, color=MUTED), title_font=dict(size=12, color=MUTED), title_standoff=10,
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig

def force_english_direction():
    """Fix: Streamlit's slider follows the browser language (Arabic = right-to-left),
    but its colored bar is always drawn left-to-right. This tells it to use English (LTR)."""
    import streamlit.components.v1 as components

    components.html(
        """
        <script>
        const w = window.parent;
        w[Symbol.for('react-aria.i18n.locale')] = 'en-US';
        try {
          Object.defineProperty(w.navigator, 'language', { get: () => 'en-US', configurable: true });
          Object.defineProperty(w.navigator, 'languages', { get: () => ['en-US', 'en'], configurable: true });
        } catch (e) {}
        w.dispatchEvent(new Event('languagechange'));
        </script>
        """,
        height=0,
    )


def space_background():
    """Three shooting stars that fly across the sides of the page."""
    html('<div class="sky"><span class="shoot s1"></span><span class="shoot s2"></span><span class="shoot s3"></span></div>')