"""
Rating Intelligence Dashboard.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.db import (get_rating_distribution, get_top_rated_products,
                      get_rating_vs_price, get_category_stats)
from utils.helpers import fmt_currency, fmt_number, truncate, rating_stars
from utils.styles import apply_theme, ORANGE_SCALE


def render():
    st.markdown("""
    <div class="section-header">
        <h2>⭐ Rating Intelligence Dashboard</h2>
        <span class="section-badge">Deep Analysis</span>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Overall Rating Distribution</div>', unsafe_allow_html=True)
        rating_df = get_rating_distribution()
        if not rating_df.empty:
            fig = px.bar(
                rating_df, x="rating_bucket", y="count",
                color="count", color_continuous_scale=ORANGE_SCALE,
                labels={"rating_bucket": "Rating", "count": "Products"},
                text="count",
            )
            fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside",
                              textfont_color="#94A3B8", marker_line_width=0)
            apply_theme(fig, height=320)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Average Rating by Category (Top 20)</div>', unsafe_allow_html=True)
        cat_df = get_category_stats().head(20)
        if not cat_df.empty:
            sorted_df = cat_df.sort_values("avg_rating", ascending=True)
            fig2 = px.bar(
                sorted_df,
                x="avg_rating", y="main_category", orientation="h",
                color="avg_rating",
                color_continuous_scale=[[0,"#1a0a00"],[0.5,"#FF9900"],[1,"#10B981"]],
                range_color=[3.5, 5],
                labels={"avg_rating": "Avg Rating", "main_category": ""},
                text="avg_rating",
            )
            fig2.update_traces(texttemplate="%{text:.2f}", textposition="outside",
                               textfont_color="#94A3B8", marker_line_width=0)
            apply_theme(fig2, height=320,
                        xaxis_kw=dict(range=[0, 5.5]))   # ✅ no conflict
            fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Rating vs Price scatter ────────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Rating vs Discount Price  — 5,000 product sample</div>',
                unsafe_allow_html=True)
    rvp = get_rating_vs_price(5000)
    if not rvp.empty:
        rvp = rvp[rvp["discount_price"].between(0, 50_000)]
        fig3 = px.scatter(
            rvp, x="discount_price", y="ratings",
            color="main_category",
            opacity=0.55,
            labels={"discount_price": "Discount Price (₹)", "ratings": "Rating",
                    "main_category": "Category"},
            hover_data=["no_of_ratings"],
            # trendline removed — requires statsmodels
        )
        fig3.update_traces(marker_size=5)
        apply_theme(fig3, height=420, showlegend=True,
                    legend_kw=dict(font=dict(size=9)))
        st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Top rated product cards ────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h2>🏆 Top Rated Products</h2></div>
    """, unsafe_allow_html=True)

    min_rev = st.slider("Minimum Reviews", 100, 10_000, 500, 100)
    top_df  = get_top_rated_products(min_reviews=min_rev, limit=32)

    if not top_df.empty:
        cols = st.columns(4)
        for i, (_, row) in enumerate(top_df.iterrows()):
            img_url = str(row.get("image", ""))
            link    = str(row.get("link", ""))
            name    = truncate(str(row.get("name", "")), 55)
            stars   = rating_stars(row.get("ratings"))
            price   = fmt_currency(row.get("discount_price"))
            rev     = fmt_number(row.get("no_of_ratings"))
            cat     = str(row.get("main_category", ""))

            img_tag = (
                f'<img src="{img_url}" style="width:100%;height:130px;object-fit:contain;'
                f'border-radius:10px;background:#1a2035;" onerror="this.style.display=\'none\'" />'
                if img_url.startswith("http") else
                '<div style="width:100%;height:130px;border-radius:10px;background:#1a2035;'
                'display:flex;align-items:center;justify-content:center;font-size:2rem;">📦</div>'
            )
            link_html = (
                f'<a href="{link}" target="_blank" style="color:#FF9900;font-size:.75rem;'
                f'font-weight:700;text-decoration:none;">🔗 Amazon</a>'
                if link.startswith("http") else ""
            )

            with cols[i % 4]:
                st.markdown(f"""
                <div class="product-card" style="margin-bottom:.75rem;">
                    {img_tag}
                    <span class="product-category" style="margin-top:.5rem;display:inline-block">{cat}</span>
                    <div class="product-name">{name}</div>
                    <div class="product-rating">{stars}</div>
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-top:.3rem;">
                        <span class="product-price">{price}</span>
                        {link_html}
                    </div>
                    <div style="color:#94A3B8;font-size:.75rem;">{rev} reviews</div>
                </div>
                """, unsafe_allow_html=True)

            if i % 4 == 3 and i < len(top_df) - 1:
                cols = st.columns(4)
