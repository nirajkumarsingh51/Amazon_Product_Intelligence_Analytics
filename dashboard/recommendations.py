"""
Product Recommendation System.
"""
import streamlit as st
import pandas as pd
import numpy as np

from utils.db import get_recommendations, get_all_categories, search_products
from utils.helpers import fmt_currency, fmt_number, truncate, rating_stars
from utils.styles import PLOTLY_THEME
import plotly.express as px


def _render_product_card(row, width_pct="100%"):
    img_url = str(row.get("image", ""))
    link    = str(row.get("link", ""))
    name    = truncate(str(row.get("name", "")), 60)
    stars   = rating_stars(row.get("ratings"))
    rat     = row.get("ratings")
    price   = fmt_currency(row.get("discount_price"))
    act_p   = fmt_currency(row.get("actual_price"))
    rev     = fmt_number(row.get("no_of_ratings"))
    cat     = str(row.get("main_category", ""))
    sub     = str(row.get("sub_category", ""))

    # compute savings
    try:
        disc = row.get("discount_price"); actual = row.get("actual_price")
        if pd.notna(disc) and pd.notna(actual) and actual > 0:
            pct = int((actual - disc) / actual * 100)
            savings_badge = f'<span style="background:#10B981;color:#fff;font-size:.68rem;font-weight:700;padding:.15rem .45rem;border-radius:999px;">-{pct}%</span>'
        else:
            savings_badge = ""
    except Exception:
        savings_badge = ""

    img_tag = (f'<img src="{img_url}" style="width:100%;height:150px;object-fit:contain;'
               f'border-radius:10px;background:#1a2035;" onerror="this.style.display=\'none\'"/>'
               if img_url.startswith("http") else
               '<div style="width:100%;height:150px;border-radius:10px;background:#1a2035;'
               'display:flex;align-items:center;justify-content:center;font-size:2.5rem;">📦</div>')
    link_html = (f'<a href="{link}" target="_blank" style="color:#FF9900;font-size:.75rem;font-weight:700;'
                 f'text-decoration:none;display:block;margin-top:.5rem;">🔗 View on Amazon →</a>'
                 if link.startswith("http") else "")

    st.markdown(f"""
    <div class="product-card" style="margin-bottom:.75rem;min-height:330px;">
        {img_tag}
        <div style="margin-top:.6rem;">
            <div style="display:flex;gap:.3rem;flex-wrap:wrap;margin-bottom:.3rem;">
                <span class="product-category">{cat}</span>
                {savings_badge}
            </div>
            <div class="product-name">{name}</div>
            <div class="product-rating" style="margin:.3rem 0;">{stars}
                <span style="color:var(--text-secondary);font-size:.75rem;">({rev})</span>
            </div>
            <div style="display:flex;align-items:baseline;gap:.5rem;">
                <span class="product-price">{price}</span>
                <span class="product-actual">{act_p}</span>
            </div>
            {link_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.markdown("""
    <div class="section-header">
        <h2>🤖 Product Recommendation System</h2>
        <span class="section-badge">AI Engine</span>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📁 Category-Based", "⭐ Rating-Based", "🔍 Similar Products"])

    # ── Tab 1: Category-Based ──────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("""
        <div style="background:rgba(255,153,0,.08);border:1px solid rgba(255,153,0,.2);
            border-radius:12px;padding:1rem;margin-bottom:1.5rem;">
            <b style="color:var(--accent-1);">🧠 How it works:</b>
            <span style="color:var(--text-secondary);font-size:.9rem;">
            Products are ranked using a composite score: <code>rating × log(reviews+1)</code>
            — balancing quality with popularity.
            </span>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns([2, 1])
        with c1:
            categories = get_all_categories()
            sel_cat    = st.selectbox("🗂️ Choose Category", [c for c in categories if c != "All"])
        with c2:
            n_recs = st.selectbox("Results", [8, 12, 16, 20], index=1)

        if st.button("🚀 Get Recommendations", key="btn_cat_rec"):
            with st.spinner("Generating recommendations…"):
                rec_df = get_recommendations(sel_cat, limit=n_recs)

            if rec_df.empty:
                st.warning("No recommendations found for this category.")
            else:
                st.markdown(f"<div style='color:var(--text-secondary);margin-bottom:1rem;font-size:.9rem;'>"
                            f"✅ Top <strong style='color:var(--accent-1)'>{len(rec_df)}</strong> recommendations for "
                            f"<strong>{sel_cat}</strong></div>", unsafe_allow_html=True)
                cols = st.columns(4)
                for i, (_, row) in enumerate(rec_df.iterrows()):
                    with cols[i % 4]:
                        _render_product_card(row)
                    if i % 4 == 3 and i < len(rec_df) - 1:
                        cols = st.columns(4)

    # ── Tab 2: Rating-Based ────────────────────────────────────────────────────
    with tabs[1]:
        c1, c2, c3 = st.columns(3)
        with c1:
            min_rating = st.slider("⭐ Min Rating", 3.0, 5.0, 4.2, 0.1, key="rec_min_rat")
        with c2:
            max_price  = st.slider("💰 Max Price (₹)", 0, 100_000, 50_000, 1_000, key="rec_max_p")
        with c3:
            n2         = st.selectbox("Results", [8, 12, 16, 24], index=1, key="n_rat_rec")

        categories2 = get_all_categories()
        sel_cat2    = st.selectbox("📁 Category (optional)", categories2, key="cat_rat_rec")

        if st.button("⭐ Find Top Rated", key="btn_rat_rec"):
            with st.spinner("Finding top-rated products…"):
                results = search_products(
                    query="", category=sel_cat2,
                    min_rating=min_rating, max_price=max_price,
                    limit=n2
                )

            if results.empty:
                st.warning("No products found. Try adjusting filters.")
            else:
                cols = st.columns(4)
                for i, (_, row) in enumerate(results.iterrows()):
                    with cols[i % 4]:
                        _render_product_card(row)
                    if i % 4 == 3 and i < len(results) - 1:
                        cols = st.columns(4)

    # ── Tab 3: Similar Products ────────────────────────────────────────────────
    with tabs[2]:
        keyword = st.text_input("🔍 Enter product keyword to find similar items",
                                placeholder="e.g. bluetooth speaker, running shoes…",
                                key="sim_search")
        c1, c2 = st.columns([2, 1])
        with c1:
            categories3 = get_all_categories()
            sel_cat3    = st.selectbox("📁 Category", categories3, key="sim_cat")
        with c2:
            n3 = st.selectbox("Results", [8, 12, 20], index=1, key="n_sim")

        if keyword and st.button("🔎 Find Similar Products", key="btn_sim"):
            with st.spinner("Finding similar products…"):
                sim_df = search_products(keyword, category=sel_cat3, limit=n3)

            if sim_df.empty:
                st.warning("No similar products found.")
            else:
                st.markdown(f"<div style='color:var(--text-secondary);margin-bottom:1rem;'>"
                            f"✅ <strong style='color:var(--accent-1)'>{len(sim_df)}</strong> similar products found</div>",
                            unsafe_allow_html=True)
                cols = st.columns(4)
                for i, (_, row) in enumerate(sim_df.iterrows()):
                    with cols[i % 4]:
                        _render_product_card(row)
                    if i % 4 == 3 and i < len(sim_df) - 1:
                        cols = st.columns(4)
