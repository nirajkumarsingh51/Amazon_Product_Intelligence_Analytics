"""
Visual Analytics page — 7 chart types, all using apply_theme.
trendline="lowess" removed (requires statsmodels).
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from utils.db import (get_category_stats, get_heatmap_data,
                      get_rating_vs_price, get_discount_analysis,
                      get_price_distribution, get_sub_category_stats)
from utils.styles import apply_theme, ORANGE_SCALE, CYAN_SCALE


def render():
    st.markdown("""
    <div class="section-header">
        <h2>📊 Visual Analytics Studio</h2>
        <span class="section-badge">7 Chart Types</span>
    </div>""", unsafe_allow_html=True)

    cat_df  = get_category_stats()
    disc_df = get_discount_analysis()

    tabs = st.tabs(["🗺️ Heatmap","🌲 Treemap","🫧 Bubble",
                    "☀️ Sunburst","📈 Scatter","📊 Histogram","🎨 Seaborn"])

    # ── 1. Heatmap ─────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Category × Price-Band Heatmap (Avg Rating)</div>',
                    unsafe_allow_html=True)
        hm_df = get_heatmap_data()
        if not hm_df.empty:
            pivot = hm_df.pivot_table(
                index="main_category", columns="price_bucket",
                values="avg_rating", aggfunc="mean"
            ).dropna(how="all", axis=1).dropna(how="all", axis=0)
            pivot = pivot.iloc[:25, :15]
            pivot.columns = [f"₹{int(c/1000)}K" for c in pivot.columns]
            fig = px.imshow(
                pivot,
                color_continuous_scale=[[0,"#0a0e1a"],[0.4,"#7C3AED"],[0.7,"#FF9900"],[1,"#10B981"]],
                aspect="auto",
                labels=dict(x="Price Band", y="Category", color="Avg Rating"),
            )
            apply_theme(fig, height=550)
            fig.update_layout(coloraxis_colorbar=dict(title="Avg Rating",
                                                       tickfont=dict(color="#94A3B8")))
            fig.update_xaxes(side="bottom")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 2. Treemap ─────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Product Treemap — Category → Sub-Category</div>',
                    unsafe_allow_html=True)
        sub_df = get_sub_category_stats()
        if not sub_df.empty:
            fig2 = px.treemap(
                sub_df.head(60), path=["main_category","sub_category"],
                values="product_count", color="avg_rating",
                color_continuous_scale=[[0,"#1a0a00"],[0.5,"#FF9900"],[1,"#10B981"]],
                hover_data={"avg_discount_price": True},
            )
            fig2.update_traces(
                textinfo="label+value",
                hovertemplate="<b>%{label}</b><br>Products: %{value:,}<extra></extra>",
            )
            apply_theme(fig2, height=500)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 3. Bubble ──────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Bubble Chart: Avg Price vs Rating (size = Products)</div>',
                    unsafe_allow_html=True)
        fig3 = px.scatter(
            cat_df[cat_df["avg_discount_price"].notna()],
            x="avg_discount_price", y="avg_rating",
            size="product_count", color="avg_discount_pct",
            hover_name="main_category", size_max=60,
            color_continuous_scale=[[0,"#001a1f"],[1,"#00D4FF"]],
            labels={"avg_discount_price":"Avg Price (₹)","avg_rating":"Avg Rating",
                    "product_count":"Products","avg_discount_pct":"Disc %"},
        )
        apply_theme(fig3, height=500)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 4. Sunburst ────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Sunburst: Category → Sub-Category (Top 40)</div>',
                    unsafe_allow_html=True)
        sub_df2 = get_sub_category_stats()
        if not sub_df2.empty:
            fig4 = px.sunburst(
                sub_df2.head(40), path=["main_category","sub_category"],
                values="product_count", color="avg_discount_price",
                color_continuous_scale=[[0,"#1a0a00"],[1,"#FF9900"]],
            )
            fig4.update_traces(
                textinfo="label+percent parent",
                hovertemplate="<b>%{label}</b><br>Products: %{value:,}<br>"
                              "Avg Price: ₹%{color:,.0f}<extra></extra>",
            )
            apply_theme(fig4, height=550)
            fig4.update_coloraxes(showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 5. Scatter (no trendline — statsmodels not installed) ──────────────────
    with tabs[4]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Rating vs Price Scatter (5K sample)</div>',
                    unsafe_allow_html=True)
        rvp = get_rating_vs_price(5000)
        if not rvp.empty:
            rvp = rvp[rvp["discount_price"].between(1, 50_000)]
            fig5 = px.scatter(
                rvp, x="discount_price", y="ratings",
                color="main_category", opacity=0.55,
                marginal_x="histogram", marginal_y="violin",
                labels={"discount_price":"Price (₹)","ratings":"Rating"},
            )
            fig5.update_traces(marker_size=4, selector=dict(mode="markers"))
            apply_theme(fig5, height=550, showlegend=True,
                        legend_kw=dict(font=dict(size=9)))
            st.plotly_chart(fig5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 6. Histogram ──────────────────────────────────────────────────────────
    with tabs[5]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Price Distribution — Box Overlay</div>',
                    unsafe_allow_html=True)
        price_df = get_price_distribution()
        if not price_df.empty:
            price_df = price_df[price_df["discount_price"].between(1, 20_000)]
            fig6 = px.histogram(
                price_df, x="discount_price", nbins=80,
                color_discrete_sequence=["#7C3AED"],
                marginal="box",
                labels={"discount_price":"Discount Price (₹)"},
            )
            apply_theme(fig6, height=400)
            fig6.update_traces(marker_line_width=0, selector=dict(type="histogram"))
            st.plotly_chart(fig6, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── 7. Seaborn ────────────────────────────────────────────────────────────
    with tabs[6]:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Seaborn: Category Avg Ratings (Top 20)</div>',
                    unsafe_allow_html=True)
        top20 = cat_df.head(20).copy()
        BG = "#111827"
        fig7, ax = plt.subplots(figsize=(10, 6), facecolor=BG)
        ax.set_facecolor(BG)
        palette = sns.color_palette("rocket", n_colors=len(top20))
        bars = ax.barh(top20["main_category"], top20["avg_rating"], color=palette)
        ax.set_xlabel("Average Rating", color="#94A3B8", fontsize=11)
        ax.set_title("Category Average Ratings", color="#F1F5F9", fontsize=14, fontweight="bold", pad=14)
        ax.tick_params(colors="#94A3B8", labelsize=9)
        for sp in ax.spines.values():
            sp.set_color("#334155")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for bar, val in zip(bars, top20["avg_rating"]):
            ax.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                    f"{val:.2f}", va="center", ha="left", color="#94A3B8", fontsize=8)
        ax.set_xlim(0, 5.5)
        ax.set_facecolor(BG)
        fig7.tight_layout()
        st.pyplot(fig7)
        plt.close(fig7)
        st.markdown("</div>", unsafe_allow_html=True)
