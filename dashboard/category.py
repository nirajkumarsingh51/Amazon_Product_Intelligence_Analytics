"""
Category Analytics page.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import (get_category_stats, get_sub_category_stats,
                      get_all_categories)
from utils.helpers import fmt_currency, fmt_number, get_category_icon
from utils.styles import apply_theme, ORANGE_SCALE, CYAN_SCALE


def render():
    st.markdown("""
    <div class="section-header">
        <h2>📁 Category Analytics</h2>
        <span class="section-badge">Drill-Down</span>
    </div>""", unsafe_allow_html=True)

    cat_df = get_category_stats()
    if cat_df.empty:
        st.error("No category data found.")
        return

    # ── Treemap ────────────────────────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Category Treemap — Product Count (colour = Avg Rating)</div>',
                unsafe_allow_html=True)
    fig_tree = px.treemap(
        cat_df.head(30), path=["main_category"], values="product_count",
        color="avg_rating",
        color_continuous_scale=[[0,"#1a0a00"],[0.5,"#FF9900"],[1,"#10B981"]],
        color_continuous_midpoint=3.5,
        custom_data=["avg_discount_price","total_reviews"],
        hover_name="main_category",
    )
    fig_tree.update_traces(
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>%{value:,} products",
        hovertemplate="<b>%{label}</b><br>Products: %{value:,}<br>"
                      "Avg Rating: %{color:.2f}<br>Avg Price: ₹%{customdata[0]:,.0f}<extra></extra>",
    )
    apply_theme(fig_tree, height=450)
    fig_tree.update_layout(coloraxis_colorbar=dict(title="Avg Rating", tickcolor="#94A3B8",
                                                    tickfont=dict(color="#94A3B8")))
    st.plotly_chart(fig_tree, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Drill-down selector ────────────────────────────────────────────────────
    col_sel, _ = st.columns([2, 3])
    with col_sel:
        categories = get_all_categories()
        sel_cat    = st.selectbox("🔍 Select Category for Drill-Down", categories,
                                  key="cat_drill")

    sub_df = get_sub_category_stats(sel_cat if sel_cat != "All" else None)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Sub-Category Sunburst</div>', unsafe_allow_html=True)
        if not sub_df.empty:
            fig2 = px.sunburst(
                sub_df.head(25),
                path=["main_category","sub_category"],
                values="product_count",
                color="avg_rating",
                color_continuous_scale=[[0,"#0d1220"],[0.5,"#7C3AED"],[1,"#FF9900"]],
                hover_data={"avg_discount_price": True},
            )
            fig2.update_traces(
                textinfo="label+percent parent",
                hovertemplate="<b>%{label}</b><br>Products: %{value:,}<br>"
                              "Avg Rating: %{color:.2f}<extra></extra>",
            )
            apply_theme(fig2, height=400)
            fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top Sub-Categories by Products</div>', unsafe_allow_html=True)
        if not sub_df.empty:
            top_sub = sub_df.head(15)
            fig3 = px.bar(
                top_sub, x="product_count", y="sub_category",
                orientation="h", color="avg_rating",
                color_continuous_scale=ORANGE_SCALE,
                labels={"product_count": "Products", "sub_category": ""},
                text="product_count",
            )
            fig3.update_traces(texttemplate="%{text:,}", textposition="outside",
                               textfont_color="#94A3B8", marker_line_width=0)
            apply_theme(fig3, height=400)
            fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Bubble ─────────────────────────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Category Intelligence: Rating vs Avg Price (bubble = product count)</div>',
                unsafe_allow_html=True)
    bubble_df = cat_df[cat_df["avg_discount_price"].notna() & cat_df["avg_rating"].notna()]
    fig4 = px.scatter(
        bubble_df, x="avg_discount_price", y="avg_rating",
        size="product_count", color="total_reviews",
        hover_name="main_category", size_max=55,
        color_continuous_scale=CYAN_SCALE,
        labels={"avg_discount_price":"Avg Discount Price (₹)","avg_rating":"Avg Rating",
                "total_reviews":"Total Reviews","product_count":"Products"},
    )
    apply_theme(fig4, height=420, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Category cards grid ────────────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>📦 All Categories</h2></div>""",
                unsafe_allow_html=True)

    cols = st.columns(4)
    for i, (_, row) in enumerate(cat_df.iterrows()):
        icon  = get_category_icon(row["main_category"])
        name  = row["main_category"]
        count = fmt_number(row["product_count"])
        rat   = f"{row['avg_rating']:.2f} ⭐" if pd.notna(row["avg_rating"]) else "N/A"
        price = fmt_currency(row["avg_discount_price"])
        with cols[i % 4]:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:.75rem;padding:1rem;">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-size:.8rem;font-weight:700;color:#F1F5F9;
                    margin:.3rem 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{name}</div>
                <div style="font-size:.75rem;color:#94A3B8;">{count} products</div>
                <div style="font-size:.75rem;color:#FF9900;">{rat}</div>
                <div style="font-size:.75rem;color:#10B981;">{price} avg</div>
            </div>
            """, unsafe_allow_html=True)
        if i % 4 == 3:
            cols = st.columns(4)
