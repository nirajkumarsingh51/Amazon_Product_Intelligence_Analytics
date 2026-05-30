"""
Executive Dashboard – KPI overview and top-level charts.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.db import (get_executive_kpis, get_category_stats,
                      get_rating_distribution, get_discount_analysis)
from utils.helpers import fmt_currency, fmt_number, get_category_icon
from utils.styles import apply_theme, ORANGE_SCALE


def _metric_card(icon, label, value, delta="", color="orange"):
    st.markdown(f"""
    <div class="metric-card {color}">
        <div class="metric-icon">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-delta'>"+delta+"</div>" if delta else ""}
    </div>
    """, unsafe_allow_html=True)


def render():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛒 Amazon Product Intelligence Platform</div>
        <div class="hero-subtitle">
            Enterprise analytics dashboard powered by 550K+ live Amazon India products.
            Track pricing, ratings, category trends and market intelligence in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Loading KPIs…"):
        kpis = get_executive_kpis()

    if not kpis:
        st.error("⚠️ Cannot connect to database. Check MySQL is running.")
        return

    total_products   = fmt_number(kpis.get("total_products", 0))
    total_categories = fmt_number(kpis.get("total_categories", 0))
    avg_rating       = f"{kpis.get('avg_rating', 0):.2f} ⭐"
    avg_disc_price   = fmt_currency(kpis.get("avg_discount_price", 0))
    avg_act_price    = fmt_currency(kpis.get("avg_actual_price", 0))
    total_reviews    = fmt_number(kpis.get("total_reviews", 0))
    avg_disc_pct     = f"{kpis.get('avg_discount_pct', 0):.1f}%"
    total_sub_cats   = fmt_number(kpis.get("total_sub_categories", 0))

    cards = [
        ("📦", "Total Products",     total_products,   "551K+ items indexed",       "orange"),
        ("📁", "Main Categories",    total_categories, f"{total_sub_cats} sub-cats", "cyan"),
        ("⭐", "Average Rating",     avg_rating,       "Across all products",        "violet"),
        ("💬", "Total Reviews",      total_reviews,    "Customer feedback",          "green"),
        ("💰", "Avg Discount Price", avg_disc_price,   "Current selling price",      "orange"),
        ("🏷️", "Avg Actual Price",   avg_act_price,    "MRP / original price",       "cyan"),
        ("🔥", "Avg Discount",       avg_disc_pct,     "Savings vs actual price",    "rose"),
        ("🛒", "Sub-categories",     total_sub_cats,   "Product segments",           "violet"),
    ]
    cols = st.columns(4)
    for i, (icon, label, val, delta, color) in enumerate(cards):
        with cols[i % 4]:
            _metric_card(icon, label, val, delta, color)
        if i % 4 == 3 and i < len(cards) - 1:
            st.markdown("<div style='margin-bottom:.75rem'/>", unsafe_allow_html=True)
            cols = st.columns(4)

    st.markdown("<br/>", unsafe_allow_html=True)

    # ── Category overview ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>📊 Category Overview</h2>
        <span class="section-badge">Live</span>
    </div>""", unsafe_allow_html=True)

    with st.spinner("Loading category data…"):
        cat_df = get_category_stats()

    if cat_df.empty:
        st.warning("No category data available.")
        return

    cat_df = cat_df[cat_df["main_category"].notna() & (cat_df["main_category"] != "")]
    top20  = cat_df.head(20)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top 20 Categories by Product Count</div>', unsafe_allow_html=True)
        fig = px.bar(
            top20, x="product_count", y="main_category", orientation="h",
            color="product_count", color_continuous_scale=ORANGE_SCALE,
            labels={"product_count": "Products", "main_category": ""},
            hover_data={"avg_rating": True, "avg_discount_price": True},
        )
        fig.update_traces(marker_line_width=0)
        apply_theme(fig, height=480, showlegend=False,
                    yaxis_kw=dict(categoryorder="total ascending"))
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Category Share — Top 12</div>', unsafe_allow_html=True)
        top12 = cat_df.head(12)
        fig2 = px.pie(
            top12, values="product_count", names="main_category", hole=0.52,
            color_discrete_sequence=["#FF9900","#00D4FF","#7C3AED","#10B981",
                                     "#F43F5E","#3B82F6","#F59E0B","#EC4899",
                                     "#06B6D4","#8B5CF6","#EF4444","#14B8A6"],
        )
        fig2.update_traces(textposition="inside", textinfo="percent",
                           marker=dict(line=dict(color="#0a0e1a", width=2)))
        apply_theme(fig2, height=480, showlegend=True,
                    legend_kw=dict(font=dict(size=10)))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Bottom row ─────────────────────────────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Rating Distribution</div>', unsafe_allow_html=True)
        rating_df = get_rating_distribution()
        if not rating_df.empty:
            fig3 = px.bar(
                rating_df, x="rating_bucket", y="count",
                color="count", color_continuous_scale=ORANGE_SCALE,
                labels={"rating_bucket": "Rating", "count": "Products"},
            )
            fig3.update_traces(marker_line_width=0)
            apply_theme(fig3, height=320, showlegend=False)
            fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Avg Discount % by Category (Top 15)</div>', unsafe_allow_html=True)
        disc_df = get_discount_analysis().head(15)
        if not disc_df.empty:
            fig4 = px.bar(
                disc_df, x="avg_discount_pct", y="main_category", orientation="h",
                color="avg_discount_pct",
                color_continuous_scale=[[0,"#1a0a00"],[1,"#F43F5E"]],
                labels={"avg_discount_pct": "Avg Discount %", "main_category": ""},
            )
            fig4.update_traces(marker_line_width=0)
            apply_theme(fig4, height=320, showlegend=False)
            fig4.update_coloraxes(showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Summary table ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header"><h2>📋 Category Summary</h2></div>
    """, unsafe_allow_html=True)

    display = cat_df.copy()
    display["icon"]     = display["main_category"].apply(get_category_icon)
    display["Category"] = display["icon"] + "  " + display["main_category"]
    display = display.rename(columns={
        "product_count": "Products", "avg_rating": "Avg Rating",
        "avg_discount_price": "Avg Price (₹)", "avg_actual_price": "Avg MRP (₹)",
        "total_reviews": "Total Reviews", "avg_discount_pct": "Discount %",
    })
    show_cols = ["Category","Products","Avg Rating","Avg Price (₹)","Avg MRP (₹)","Total Reviews","Discount %"]
    st.dataframe(
        display[show_cols].head(50),
        use_container_width=True, height=440,
        column_config={
            "Avg Rating":  st.column_config.ProgressColumn("Avg Rating",  min_value=0, max_value=5,   format="%.2f"),
            "Discount %":  st.column_config.ProgressColumn("Discount %",  min_value=0, max_value=100, format="%.1f%%"),
        },
        hide_index=True,
    )
