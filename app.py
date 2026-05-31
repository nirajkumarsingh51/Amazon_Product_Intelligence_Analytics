"""
Amazon Product Intelligence & Analytics Platform
================================================
Enterprise-grade Streamlit dashboard (Responsive version)
"""

import streamlit as st

# ── Page config (MUST be first) ─────────────────────────────
st.set_page_config(
    page_title="Amazon Product Intelligence Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",  # FIXED for mobile
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Amazon Product Intelligence & Analytics Platform",
    },
)

# ── Mobile Responsive Fix (INLINE CSS) ───────────────────────
st.markdown("""
<style>
@media (max-width: 768px) {

    .block-container {
        padding: 0.8rem !important;
    }

    section[data-testid="stSidebar"] {
        width: 280px !important;
        min-width: 280px !important;
    }

    .stRadio label {
        font-size: 14px !important;
    }

    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.3rem !important; }
    h3 { font-size: 1.1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Global CSS ───────────────────────────────────────────────
from utils.styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:1rem 0;">
        <div style="font-size:2.2rem;">🛒</div>
        <div style="font-size:1rem;font-weight:800;
            background:linear-gradient(90deg,#FF9900,#00D4FF);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            Amazon Product<br>Intelligence
        </div>
        <div style="font-size:.7rem;color:#64748B;">
            Analytics Platform
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,.08);"/>
    """, unsafe_allow_html=True)

    NAV_ITEMS = {
        "🏠 Executive Dashboard": "executive",
        "🔍 Product Search Engine": "search",
        "📁 Category Analytics": "category",
        "💰 Price Intelligence": "price",
        "⭐ Rating Intelligence": "ratings",
        "🤖 Recommendations": "recommendations",
        "📊 Visual Analytics": "visual",
        "🖼️ Product Gallery": "gallery",
        "🧠 AI Insights": "ai_insights",
        "⬇️ Download Center": "downloads",
    }

    selected_label = st.radio(
        "Navigation",
        list(NAV_ITEMS.keys()),
        label_visibility="collapsed",
    )

    page = NAV_ITEMS[selected_label]

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,.08);margin:1rem 0;"/>
    <div style="font-size:.75rem;color:#94A3B8;">
        📦 551,585+ Products<br>
        📁 113 Categories<br>
        🗄️ MySQL · Streamlit · Plotly<br>
        <b>v1.0.0 Production</b>
    </div>
    """, unsafe_allow_html=True)

# ── Page routing ────────────────────────────────────────────
def load_page(page):
    if page == "executive":
        from dashboard.executive import render
    elif page == "search":
        from dashboard.search import render
    elif page == "category":
        from dashboard.category import render
    elif page == "price":
        from dashboard.price import render
    elif page == "ratings":
        from dashboard.ratings import render
    elif page == "recommendations":
        from dashboard.recommendations import render
    elif page == "visual":
        from dashboard.visual_analytics import render
    elif page == "gallery":
        from dashboard.gallery import render
    elif page == "ai_insights":
        from dashboard.ai_insights import render
    elif page == "downloads":
        from dashboard.downloads import render
    else:
        from dashboard.executive import render

    render()

load_page(page)
