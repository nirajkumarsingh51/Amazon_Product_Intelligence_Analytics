"""
Amazon Product Intelligence & Analytics Platform
================================================
Enterprise-grade Streamlit analytics dashboard.
"""

import streamlit as st

# ── Page config (must be FIRST streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="Amazon Product Intelligence Platform",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "Amazon Product Intelligence & Analytics Platform — Built with ❤️ using Streamlit",
    },
)

# ── Inject global CSS ──────────────────────────────────────────────────────────
from utils.styles import GLOBAL_CSS
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Sidebar navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.5rem 0 1rem;">
        <div style="font-size:2.5rem;">🛒</div>
        <div style="font-size:1rem;font-weight:800;
            background:linear-gradient(90deg,#FF9900,#00D4FF);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            line-height:1.2;margin-top:.4rem;">Amazon Product<br>Intelligence</div>
        <div style="font-size:.7rem;color:#64748B;margin-top:.3rem;letter-spacing:.1em;text-transform:uppercase;">
            Analytics Platform
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,.08);margin:.5rem 0 1rem;"/>
    """, unsafe_allow_html=True)

    NAV_ITEMS = {
        "🏠  Executive Dashboard":        "executive",
        "🔍  Product Search Engine":      "search",
        "📁  Category Analytics":         "category",
        "💰  Price Intelligence":         "price",
        "⭐  Rating Intelligence":        "ratings",
        "🤖  Recommendations":            "recommendations",
        "📊  Visual Analytics":           "visual",
        "🖼️  Product Gallery":            "gallery",
        "🧠  AI Insights":                "ai_insights",
        "⬇️  Download Center":            "downloads",
    }

    selected_label = st.radio(
        "Navigation",
        list(NAV_ITEMS.keys()),
        label_visibility="collapsed",
    )
    page = NAV_ITEMS[selected_label]

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,.08);margin:1rem 0 .75rem;"/>
    <div style="padding:.5rem 0;color:#475569;font-size:.72rem;line-height:1.6;">
        <div>📦 <b style="color:#94A3B8;">551,585+</b> Products</div>
        <div>📁 <b style="color:#94A3B8;">113</b> Categories</div>
        <div>🗄️ MySQL · Streamlit · Plotly</div>
        <div style="margin-top:.5rem;color:#334155;">v1.0.0 — Production</div>
    </div>
    """, unsafe_allow_html=True)

# ── Route to page ──────────────────────────────────────────────────────────────
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
