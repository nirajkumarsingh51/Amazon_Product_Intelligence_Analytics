"""
Price Intelligence Dashboard.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.db import (get_price_distribution, get_cheapest_products,
                      get_most_expensive_products, get_category_stats,
                      get_discount_analysis)
from utils.helpers import fmt_currency, fmt_number, truncate
from utils.styles import apply_theme, ORANGE_SCALE, CYAN_SCALE


def render():
    st.markdown("""
    <div class="section-header">
        <h2>💰 Price Intelligence Dashboard</h2>
        <span class="section-badge">Real-time</span>
    </div>""", unsafe_allow_html=True)

    # ── Price histogram ────────────────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Discount Price Distribution (₹0 – ₹50,000)</div>',
                unsafe_allow_html=True)
    price_df = get_price_distribution()
    if not price_df.empty:
        price_df = price_df[price_df["discount_price"].between(1, 50_000)]
        fig = px.histogram(
            price_df, x="discount_price", nbins=60,
            color_discrete_sequence=["#FF9900"],
            labels={"discount_price": "Discount Price (₹)"},
        )
        apply_theme(fig, height=300)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Category price comparison ──────────────────────────────────────────────
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Category-wise Price Comparison (Top 20)</div>',
                unsafe_allow_html=True)
    cat_df = get_category_stats().head(20)
    if not cat_df.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            name="Avg Actual Price (MRP)",
            x=cat_df["main_category"], y=cat_df["avg_actual_price"],
            marker_color="#94A3B8", marker_line_width=0,
        ))
        fig2.add_trace(go.Bar(
            name="Avg Discount Price",
            x=cat_df["main_category"], y=cat_df["avg_discount_price"],
            marker_color="#FF9900", marker_line_width=0,
        ))
        apply_theme(fig2, height=360, showlegend=True,
                    xaxis_kw=dict(tickangle=-35),
                    legend_kw=dict(orientation="h", yanchor="bottom", y=1.02))
        fig2.update_layout(barmode="group")
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Discount analysis ──────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    disc_df = get_discount_analysis().head(20)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Avg Discount % by Category</div>', unsafe_allow_html=True)
        if not disc_df.empty:
            fig3 = px.bar(
                disc_df, x="avg_discount_pct", y="main_category", orientation="h",
                color="avg_discount_pct",
                color_continuous_scale=[[0,"#0a1a2e"],[1,"#F43F5E"]],
                labels={"avg_discount_pct": "Avg Discount %", "main_category": ""},
                text="avg_discount_pct",
            )
            fig3.update_traces(texttemplate="%{text:.1f}%", textposition="outside",
                               marker_line_width=0)
            apply_theme(fig3, height=480)
            fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Max Discount % by Category</div>', unsafe_allow_html=True)
        if not disc_df.empty:
            fig4 = px.bar(
                disc_df.sort_values("max_discount_pct", ascending=False).head(15),
                x="max_discount_pct", y="main_category", orientation="h",
                color="max_discount_pct",
                color_continuous_scale=[[0,"#001a1f"],[1,"#00D4FF"]],
                labels={"max_discount_pct": "Max Discount %", "main_category": ""},
            )
            fig4.update_traces(marker_line_width=0)
            apply_theme(fig4, height=480)
            fig4.update_coloraxes(showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Cheapest / expensive tables ────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>🏷️ Cheapest Products</h2></div>""",
                unsafe_allow_html=True)
    _product_table(get_cheapest_products(20))

    st.markdown("""<div class="section-header"><h2>💎 Most Expensive Products</h2></div>""",
                unsafe_allow_html=True)
    _product_table(get_most_expensive_products(20))


def _product_table(df: pd.DataFrame):
    if df.empty:
        st.info("No data available.")
        return
    display = df.copy()
    display["Discount Price"] = display["discount_price"].apply(fmt_currency)
    display["Actual Price"]   = display["actual_price"].apply(fmt_currency)
    display["Rating"] = display["ratings"].apply(
        lambda x: f"{x:.1f} ⭐" if pd.notna(x) and x > 0 else "N/A")
    display["Reviews"] = display["no_of_ratings"].apply(fmt_number)
    display["Product"] = display["name"].apply(lambda x: truncate(str(x), 70))
    show = ["Product","main_category","sub_category","Rating","Reviews","Discount Price","Actual Price"]
    st.dataframe(
        display[show].rename(columns={"main_category":"Category","sub_category":"Sub-Cat"}),
        use_container_width=True, height=380, hide_index=True,
    )
