"""
Global CSS / HTML theming for the Streamlit dashboard.
"""

GLOBAL_CSS = """
<style>
/* ── Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

/* ── Root variables ─────────────────────────────────── */
:root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #111827;
    --bg-card:       rgba(255,255,255,0.05);
    --bg-card-hover: rgba(255,255,255,0.09);
    --accent-1:      #FF9900;
    --accent-2:      #00D4FF;
    --accent-3:      #7C3AED;
    --accent-4:      #10B981;
    --accent-5:      #F43F5E;
    --text-primary:  #F1F5F9;
    --text-secondary:#94A3B8;
    --border:        rgba(255,255,255,0.09);
    --glow-orange:   0 0 40px rgba(255,153,0,0.25);
    --glow-cyan:     0 0 40px rgba(0,212,255,0.20);
    --radius:        16px;
    --font-main:     'Plus Jakarta Sans', sans-serif;
    --font-mono:     'Space Grotesk', sans-serif;
}

/* ── FORCE dark background everywhere ───────────────── */
html { background: #0a0e1a !important; }
body { background: #0a0e1a !important; }

/* Streamlit root containers */
.stApp,
.stApp > div,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section[data-testid="stMain"],
.main,
.main > div,
.block-container {
    background-color: #0a0e1a !important;
    color: #F1F5F9 !important;
}

/* Global text override */
*, *::before, *::after {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
p, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: #F1F5F9 !important;
}

/* ── Hide Streamlit chrome ──────────────────────────── */
#MainMenu { visibility: hidden !important; }
footer    { visibility: hidden !important; }
header    { visibility: hidden !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

/* ── Sidebar ────────────────────────────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebarContent"] {
    background: #0d1220 !important;
    background-image: linear-gradient(180deg, #0d1220 0%, #111827 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stRadio label { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stRadio label span { color: #94A3B8 !important; }

/* Radio selected state */
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] input:checked + div {
    background-color: #FF9900 !important;
    border-color: #FF9900 !important;
}

/* ── Metric cards ────────────────────────────────────── */
.metric-card {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
    padding: 1.4rem 1.6rem !important;
    transition: transform .2s, background .2s, box-shadow .2s !important;
    backdrop-filter: blur(12px) !important;
    position: relative !important;
    overflow: hidden !important;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.metric-card:hover {
    transform: translateY(-4px) !important;
    background: rgba(255,255,255,0.09) !important;
}
.metric-card.orange::before { background: #FF9900 !important; }
.metric-card.cyan::before   { background: #00D4FF !important; }
.metric-card.violet::before { background: #7C3AED !important; }
.metric-card.green::before  { background: #10B981 !important; }
.metric-card.rose::before   { background: #F43F5E !important; }
.metric-card.blue::before   { background: #3B82F6 !important; }

.metric-icon  { font-size: 2.2rem !important; margin-bottom: .5rem !important; }
.metric-label {
    font-size: .75rem !important; font-weight: 600 !important;
    color: #94A3B8 !important; text-transform: uppercase !important;
    letter-spacing: .1em !important; margin-bottom: .3rem !important;
}
.metric-value {
    font-size: 1.9rem !important; font-weight: 800 !important;
    color: #F1F5F9 !important; line-height: 1 !important;
}
.metric-delta { font-size: .8rem !important; color: #10B981 !important; margin-top: .4rem !important; }

/* ── Section headers ─────────────────────────────────── */
.section-header {
    display: flex !important; align-items: center !important; gap: .75rem !important;
    margin: 2rem 0 1rem !important;
    padding-bottom: .75rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.09) !important;
}
.section-header h2 {
    margin: 0 !important; font-size: 1.4rem !important; font-weight: 700 !important;
    color: #F1F5F9 !important;
}
.section-badge {
    background: #FF9900 !important;
    color: #000 !important; font-size: .65rem !important; font-weight: 700 !important;
    padding: .25rem .6rem !important; border-radius: 999px !important;
    text-transform: uppercase !important; letter-spacing: .08em !important;
}

/* ── Product cards ───────────────────────────────────── */
.product-card {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
    padding: 1rem !important;
    transition: transform .2s, box-shadow .2s !important;
    height: 100% !important;
}
.product-card:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 0 40px rgba(0,212,255,0.20) !important;
    border-color: #00D4FF !important;
}
.product-name {
    font-size: .85rem !important; font-weight: 600 !important;
    color: #F1F5F9 !important; margin: .6rem 0 .3rem !important;
    display: -webkit-box !important; -webkit-line-clamp: 2 !important;
    -webkit-box-orient: vertical !important; overflow: hidden !important;
}
.product-rating { color: #FF9900 !important; font-size: .85rem !important; }
.product-price  { color: #10B981 !important; font-weight: 700 !important; font-size: 1rem !important; }
.product-actual { color: #94A3B8 !important; text-decoration: line-through !important; font-size: .8rem !important; }
.product-category {
    background: rgba(124,58,237,.25) !important; color: #a78bfa !important;
    font-size: .7rem !important; font-weight: 600 !important;
    padding: .2rem .55rem !important; border-radius: 999px !important;
    display: inline-block !important; margin-bottom: .4rem !important;
}

/* ── Hero banner ─────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0d1220 0%, #1a0a3d 50%, #0a1a2e 100%) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 20px !important;
    padding: 3rem 3.5rem !important;
    margin-bottom: 2rem !important;
    position: relative !important;
    overflow: hidden !important;
}
.hero-banner::after {
    content: '📦';
    position: absolute;
    right: 3rem; top: 50%;
    transform: translateY(-50%);
    font-size: 8rem; opacity: .06;
}
.hero-title {
    font-size: 2.2rem !important; font-weight: 800 !important;
    background: linear-gradient(90deg, #FF9900, #00D4FF) !important;
    -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
    margin-bottom: .5rem !important;
}
.hero-subtitle { color: #94A3B8 !important; font-size: 1rem !important; max-width: 520px !important; }

/* ── Chart container ─────────────────────────────────── */
.chart-container {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
    padding: 1.2rem 1rem .5rem !important;
    margin-bottom: 1.5rem !important;
}
.chart-title {
    font-size: .9rem !important; font-weight: 700 !important;
    color: #94A3B8 !important; margin-bottom: .8rem !important;
    text-transform: uppercase !important; letter-spacing: .08em !important;
}

/* ── Streamlit widget overrides ──────────────────────── */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input {
    background-color: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #F1F5F9 !important;
}
div[data-baseweb="select"] * { color: #F1F5F9 !important; }
div[data-baseweb="popover"] {
    background: #111827 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}
div[data-baseweb="option"]:hover { background: rgba(255,153,0,0.15) !important; }

/* Slider */
[data-testid="stSlider"] * { color: #F1F5F9 !important; }

/* Tabs */
[data-testid="stTabs"] button {
    background: transparent !important;
    color: #94A3B8 !important;
    border-bottom: 2px solid transparent !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #FF9900 !important;
    border-bottom: 2px solid #FF9900 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #FF9900, #e68000) !important;
    color: #000 !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
    padding: .55rem 1.5rem !important;
}
.stButton > button:hover { opacity: .85 !important; }
.stDownloadButton > button {
    background: linear-gradient(90deg, #7C3AED, #5b21b6) !important;
    color: #fff !important; font-weight: 700 !important;
    border: none !important; border-radius: 10px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
}

/* Native st.metric */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
}
div[data-testid="stMetric"] label { color: #94A3B8 !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #F1F5F9 !important; }

/* Divider */
hr { border-color: rgba(255,255,255,0.09) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: rgba(255,153,0,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #FF9900; }
</style>
"""

# ── Plotly theme — NO xaxis/yaxis/legend keys here ────────────────────────────
# Those are applied separately via fig.update_xaxes / fig.update_yaxes to avoid
# the "multiple values for keyword argument" error.
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#94A3B8", size=12),
    margin=dict(l=40, r=20, t=40, b=40),
    colorway=["#FF9900", "#00D4FF", "#7C3AED", "#10B981", "#F43F5E", "#3B82F6", "#F59E0B"],
)

# Shared axis / legend defaults — apply with fig.update_xaxes / update_yaxes / update_layout separately
AXIS_STYLE = dict(gridcolor="rgba(255,255,255,0.06)", linecolor="rgba(255,255,255,0.1)",
                  tickcolor="#94A3B8", zerolinecolor="rgba(255,255,255,0.06)")
LEGEND_STYLE = dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(255,255,255,0.1)",
                    font=dict(color="#94A3B8", size=11))

COLOR_SCALE  = [[0, "#0a0e1a"], [0.5, "#7C3AED"], [1, "#FF9900"]]
ORANGE_SCALE = [[0, "#1a0a00"], [1, "#FF9900"]]
CYAN_SCALE   = [[0, "#001a1f"], [1, "#00D4FF"]]


def apply_theme(fig, height: int = 400, showlegend: bool = False,
                xaxis_kw: dict = None, yaxis_kw: dict = None,
                legend_kw: dict = None, **extra):
    """
    Apply the dark Plotly theme to any figure without keyword conflicts.
    Pass per-chart axis/legend overrides via xaxis_kw / yaxis_kw / legend_kw.
    """
    fig.update_layout(**PLOTLY_THEME, height=height, showlegend=showlegend, **extra)
    fig.update_xaxes(**AXIS_STYLE, **(xaxis_kw or {}))
    fig.update_yaxes(**AXIS_STYLE, **(yaxis_kw or {}))
    if showlegend or legend_kw:
        fig.update_layout(legend={**LEGEND_STYLE, **(legend_kw or {})})
    return fig
