"""
Global CSS + Plotly Theme for Streamlit Dashboard
"""

GLOBAL_CSS = """
<style>

/* ================= GOOGLE FONTS ================= */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ================= ROOT ================= */
:root {
    --bg: #0a0e1a;
    --card: rgba(255,255,255,0.06);
    --card-hover: rgba(255,255,255,0.10);
    --text: #F1F5F9;
    --muted: #94A3B8;
    --orange: #FF9900;
    --cyan: #00D4FF;
    --border: rgba(255,255,255,0.10);
}

/* ================= GLOBAL ================= */
html, body, .stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.block-container {
    padding: 1.2rem 2rem !important;
    max-width: 1400px !important;
}

/* ================= STREAMLIT DEFAULT UI HIDE ================= */
#MainMenu, footer, header {
    visibility: hidden !important;
}

/* ================= SIDEBAR FIX (NAVBAR ISSUE FIXED HERE) ================= */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1220, #111827) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 280px !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* Sidebar radio buttons FIX (THIS FIXES NAV NOT SHOWING PROPERLY) */
.stRadio > div {
    background: transparent !important;
    gap: 6px !important;
}

.stRadio label {
    padding: 10px 12px !important;
    border-radius: 10px !important;
    transition: 0.2s ease;
    color: var(--muted) !important;
}

.stRadio label:hover {
    background: var(--card) !important;
    color: var(--text) !important;
}

/* selected radio */
.stRadio input:checked + div {
    background: rgba(255,153,0,0.15) !important;
    border: 1px solid var(--orange) !important;
    color: var(--orange) !important;
}

/* ================= CARDS ================= */
.card, .metric-card, .product-card {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    transition: 0.2s ease !important;
}

.card:hover, .product-card:hover {
    background: var(--card-hover) !important;
    transform: translateY(-3px);
}

/* ================= TEXT ================= */
h1, h2, h3 {
    color: var(--text) !important;
}

p, span, label {
    color: var(--muted) !important;
}

/* ================= BUTTONS ================= */
.stButton > button {
    background: linear-gradient(90deg, #FF9900, #e67e00) !important;
    color: black !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    border: none !important;
}

.stButton > button:hover {
    opacity: 0.85;
}

/* ================= DATAFRAME ================= */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden;
}

/* ================= SCROLLBAR ================= */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: var(--orange);
    border-radius: 10px;
}

</style>
"""

# ================= PLOTLY THEME =================
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#94A3B8"),
    margin=dict(l=40, r=20, t=40, b=40),
    colorway=["#FF9900", "#00D4FF", "#7C3AED", "#10B981", "#F43F5E"],
)

AXIS_STYLE = dict(
    gridcolor="rgba(255,255,255,0.06)",
    linecolor="rgba(255,255,255,0.1)",
    tickcolor="#94A3B8"
)

LEGEND_STYLE = dict(
    bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94A3B8")
)

def apply_theme(fig, height=400, showlegend=False, **kwargs):
    fig.update_layout(**PLOTLY_THEME, height=height, showlegend=showlegend, **kwargs)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)

    if showlegend:
        fig.update_layout(legend=LEGEND_STYLE)

    return fig
