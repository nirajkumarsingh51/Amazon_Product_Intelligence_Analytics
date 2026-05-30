"""
Product Gallery – Amazon-style image grid with hover effects.
"""
import streamlit as st
import pandas as pd

from utils.db import get_gallery_products, get_all_categories
from utils.helpers import fmt_currency, fmt_number, truncate, rating_stars


def render():
    st.markdown("""
    <div class="section-header">
        <h2>🖼️ Product Gallery</h2>
        <span class="section-badge">Visual Showcase</span>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        categories = get_all_categories()
        sel_cat    = st.selectbox("📁 Category", categories, key="gallery_cat")
    with c2:
        n_products = st.selectbox("Show", [12, 24, 36, 48], index=1)
    with c3:
        sort_by = st.selectbox("Sort by", ["Popularity", "Rating", "Price ↑", "Price ↓"])

    with st.spinner("Loading products…"):
        df = get_gallery_products(sel_cat, limit=n_products)

    if df.empty:
        st.info("No products with images found in this category.")
        return

    # Sort
    if sort_by == "Rating" and "ratings" in df.columns:
        df = df.sort_values("ratings", ascending=False)
    elif sort_by == "Price ↑" and "discount_price" in df.columns:
        df = df.sort_values("discount_price", ascending=True)
    elif sort_by == "Price ↓" and "discount_price" in df.columns:
        df = df.sort_values("discount_price", ascending=False)

    st.markdown(f"<div style='color:var(--text-secondary);font-size:.85rem;margin-bottom:1rem;'>"
                f"Showing <strong style='color:var(--accent-1)'>{len(df)}</strong> products"
                f"{' in '+sel_cat if sel_cat != 'All' else ''}</div>",
                unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (_, row) in enumerate(df.iterrows()):
        img_url = str(row.get("image", ""))
        link    = str(row.get("link", ""))
        name    = truncate(str(row.get("name", "")), 55)
        stars   = rating_stars(row.get("ratings"))
        price   = fmt_currency(row.get("discount_price"))
        act_p   = fmt_currency(row.get("actual_price"))
        rev     = fmt_number(row.get("no_of_ratings"))
        cat     = str(row.get("main_category", ""))
        sub     = str(row.get("sub_category", ""))

        # Savings badge
        try:
            d = row.get("discount_price"); a = row.get("actual_price")
            if pd.notna(d) and pd.notna(a) and a > 0 and a > d:
                pct = int((a - d) / a * 100)
                badge = (f'<div style="position:absolute;top:.5rem;right:.5rem;'
                         f'background:#F43F5E;color:#fff;font-size:.65rem;font-weight:700;'
                         f'padding:.15rem .4rem;border-radius:999px;z-index:2;">-{pct}%</div>')
            else:
                badge = ""
        except Exception:
            badge = ""

        img_tag = (f'<img src="{img_url}" style="width:100%;height:155px;object-fit:contain;'
                   f'border-radius:10px;background:#1a2035;display:block;" '
                   f'onerror="this.src=\'https://via.placeholder.com/200x155/1a2035/444?text=📦\'" />'
                   if img_url.startswith("http") else
                   '<div style="width:100%;height:155px;border-radius:10px;background:#1a2035;'
                   'display:flex;align-items:center;justify-content:center;font-size:3rem;">📦</div>')

        link_open = f'href="{link}" target="_blank"' if link.startswith("http") else 'href="#"'

        with cols[i % 4]:
            st.markdown(f"""
            <a {link_open} style="text-decoration:none;">
            <div class="product-card" style="margin-bottom:.75rem;position:relative;cursor:pointer;">
                {badge}
                {img_tag}
                <span class="product-category" style="margin-top:.5rem;display:inline-block;">{cat}</span>
                <div class="product-name">{name}</div>
                <div class="product-rating">{stars}
                    <span style="color:var(--text-secondary);font-size:.72rem;"> ({rev})</span>
                </div>
                <div style="display:flex;align-items:baseline;gap:.5rem;margin-top:.2rem;">
                    <span class="product-price">{price}</span>
                    <span class="product-actual">{act_p}</span>
                </div>
            </div>
            </a>
            """, unsafe_allow_html=True)

        if i % 4 == 3 and i < len(df) - 1:
            cols = st.columns(4)
