"""
Product Search Engine page.
"""
import streamlit as st
import pandas as pd

from utils.db import search_products, get_all_categories
from utils.helpers import fmt_currency, fmt_number, truncate, rating_stars


def _product_row(row):
    """Render a single product row as a styled card."""
    img_html = ""
    if pd.notna(row.get("image")) and str(row["image"]).startswith("http"):
        img_html = f'<img src="{row["image"]}" style="width:70px;height:70px;object-fit:contain;border-radius:8px;background:#1a2035;float:left;margin-right:1rem;"/>'

    disc_p = fmt_currency(row.get("discount_price"))
    act_p  = fmt_currency(row.get("actual_price"))
    rat    = row.get("ratings")
    stars  = rating_stars(rat) if pd.notna(rat) else "N/A"
    rev    = fmt_number(row.get("no_of_ratings"))
    name   = truncate(str(row.get("name", "")), 80)
    cat    = str(row.get("main_category", ""))
    sub    = str(row.get("sub_category", ""))
    link   = str(row.get("link", ""))

    link_btn = f'<a href="{link}" target="_blank" style="color:#FF9900;font-weight:700;font-size:.8rem;text-decoration:none;">🔗 View on Amazon</a>' if link.startswith("http") else ""

    st.markdown(f"""
    <div class="product-card" style="display:flex;flex-direction:column;gap:.4rem;margin-bottom:.75rem;">
        <div style="display:flex;gap:1rem;align-items:flex-start;">
            {img_html}
            <div style="flex:1;">
                <span class="product-category">{cat}</span>
                {"<span class='product-category' style='background:rgba(0,212,255,.15);color:#67e8f9;margin-left:.3rem'>"+sub+"</span>" if sub and sub != "nan" else ""}
                <div class="product-name" style="-webkit-line-clamp:3;">{name}</div>
                <div style="display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:.4rem;">
                    <span class="product-rating">{stars} <span style="color:#94A3B8;font-size:.8rem">({rev} reviews)</span></span>
                    <span class="product-price">{disc_p}</span>
                    <span class="product-actual">{act_p}</span>
                    {link_btn}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.markdown("""
    <div class="section-header">
        <h2>🔍 Product Search Engine</h2>
        <span class="section-badge">AI-Powered</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Filters ────────────────────────────────────────────────────────────────
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            query = st.text_input("🔍 Search Products",
                                  placeholder="e.g. wireless headphones, cricket bat, yoga mat…",
                                  help="Enter any product name or keyword")
        with col2:
            categories = get_all_categories()
            category   = st.selectbox("📁 Category", categories, index=0)
        with col3:
            limit = st.selectbox("Results", [25, 50, 100], index=0)

    col4, col5 = st.columns(2)
    with col4:
        min_rating = st.slider("⭐ Minimum Rating", 0.0, 5.0, 0.0, 0.5)
    with col5:
        max_price = st.slider("💰 Max Price (₹)", 0, 200_000, 200_000, 1_000)

    search_btn = st.button("🚀 Search Products", use_container_width=False)

    if not query and not search_btn:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:var(--text-secondary);">
            <div style="font-size:4rem;">🔍</div>
            <div style="font-size:1.2rem;font-weight:600;margin-top:1rem;">
                Start by typing a product name above
            </div>
            <div style="margin-top:.5rem;font-size:.9rem;">
                Search across 551,585+ Amazon products
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    if query or search_btn:
        with st.spinner(f"Searching for '{query}'…"):
            results = search_products(
                query=query, category=category,
                min_rating=min_rating, max_price=max_price,
                limit=limit
            )

        if results.empty:
            st.warning("No products found. Try a different keyword or relax the filters.")
            return

        st.markdown(f"""
        <div style="margin:.75rem 0 1.25rem;color:var(--text-secondary);font-size:.9rem;">
            ✅ Found <strong style="color:var(--accent-1)">{len(results)}</strong> products
            {"for <strong>"+query+"</strong>" if query else ""}
        </div>
        """, unsafe_allow_html=True)

        # Tabs: card view / table view
        tab1, tab2 = st.tabs(["🃏 Card View", "📊 Table View"])

        with tab1:
            for _, row in results.iterrows():
                _product_row(row)

        with tab2:
            display = results.copy()
            display["Rating"] = display["ratings"].apply(
                lambda x: f"{x:.1f} ⭐" if pd.notna(x) and x > 0 else "N/A")
            display["Discount Price"] = display["discount_price"].apply(fmt_currency)
            display["Actual Price"]   = display["actual_price"].apply(fmt_currency)
            display["Reviews"]        = display["no_of_ratings"].apply(fmt_number)
            show = ["name", "main_category", "sub_category",
                    "Rating", "Reviews", "Discount Price", "Actual Price"]
            st.dataframe(display[show].rename(columns={
                "name": "Product", "main_category": "Category", "sub_category": "Sub-Category"
            }), use_container_width=True, height=500, hide_index=True)

        # Download
        st.markdown("---")
        dl1, dl2, _ = st.columns([1, 1, 3])
        with dl1:
            from utils.helpers import to_csv_bytes
            st.download_button("⬇️ Download CSV", to_csv_bytes(results),
                               file_name=f"search_{query[:20]}.csv",
                               mime="text/csv", use_container_width=True)
        with dl2:
            from utils.helpers import to_excel_bytes
            st.download_button("📊 Download Excel", to_excel_bytes(results),
                               file_name=f"search_{query[:20]}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)
