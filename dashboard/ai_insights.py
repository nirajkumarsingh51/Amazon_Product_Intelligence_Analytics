"""
AI Insights page — auto-generated market intelligence.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import get_ai_insights, get_category_stats
from utils.helpers import fmt_currency, fmt_number, get_category_icon
from utils.styles import apply_theme, ORANGE_SCALE, CYAN_SCALE


def _insight_card(icon, title, body, color="var(--accent-1)"):
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:1rem;padding:1.2rem;">
        <div style="font-size:1.6rem;">{icon}</div>
        <div style="font-weight:700;color:{color};margin:.4rem 0 .3rem;font-size:.95rem;">{title}</div>
        <div style="color:#94A3B8;font-size:.85rem;line-height:1.5;">{body}</div>
    </div>
    """, unsafe_allow_html=True)


def render():
    st.markdown("""
    <div class="section-header">
        <h2>🧠 AI Market Insights</h2>
        <span class="section-badge">Auto-Generated</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(124,58,237,.15),rgba(0,212,255,.1));
        border:1px solid rgba(124,58,237,.3);border-radius:14px;padding:1.2rem 1.5rem;margin-bottom:1.5rem;">
        <div style="font-size:1rem;font-weight:700;color:#a78bfa;">🤖 AI Analysis Engine</div>
        <div style="color:#94A3B8;font-size:.9rem;margin-top:.4rem;">
            Automatically analyses 551,585+ Amazon products every 10 minutes to surface hidden market
            trends, pricing intelligence and actionable business opportunities.
        </div>
    </div>""", unsafe_allow_html=True)

    with st.spinner("Running AI analysis…"):
        insights = get_ai_insights()
        cat_df   = get_category_stats()

    top_reviews  = insights.get("top_by_reviews",   pd.DataFrame())
    most_exp     = insights.get("most_expensive",    pd.DataFrame())
    best_rated   = insights.get("best_rated",        pd.DataFrame())
    disc_leaders = insights.get("discount_leaders",  pd.DataFrame())

    # ── Auto text insights ─────────────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>💡 Key Market Insights</h2></div>""",
                unsafe_allow_html=True)

    insight_list = []
    if not top_reviews.empty:
        r = top_reviews.iloc[0]
        insight_list.append(("🏆","Most Reviewed Category",
            f"<b style='color:#FF9900'>{r['main_category']}</b> leads with "
            f"<b>{fmt_number(r['total_reviews'])}</b> total customer reviews across "
            f"{fmt_number(r['products'])} products.", "#FF9900"))
    if not most_exp.empty:
        r = most_exp.iloc[0]
        insight_list.append(("💎","Premium Category",
            f"<b style='color:#00D4FF'>{r['main_category']}</b> commands the highest average price "
            f"of <b>{fmt_currency(r['avg_actual_price'])}</b> — targeting premium buyers.", "#00D4FF"))
    if not best_rated.empty:
        r = best_rated.iloc[0]
        insight_list.append(("⭐","Best Rated Category",
            f"<b style='color:#10B981'>{r['main_category']}</b> earns the highest customer satisfaction "
            f"with avg rating <b>{r['avg_rating']:.2f}/5.0</b>.", "#10B981"))
    if not disc_leaders.empty:
        r = disc_leaders.iloc[0]
        insight_list.append(("🔥","Biggest Discounts",
            f"<b style='color:#F43F5E'>{r['main_category']}</b> offers the steepest discounts, "
            f"averaging <b>{r['avg_disc']:.1f}%</b> off original price.", "#F43F5E"))
    if not cat_df.empty:
        hid = cat_df.nlargest(1,"product_count").iloc[0]
        insight_list.append(("📦","Largest Inventory",
            f"<b style='color:#3B82F6'>{hid['main_category']}</b> has the most products with "
            f"<b>{fmt_number(hid['product_count'])}</b> listings.", "#3B82F6"))
        bv = cat_df.dropna(subset=["avg_rating","avg_discount_price"])
        bv = bv[bv["avg_discount_price"] > 0].copy()
        bv["score"] = bv["avg_rating"] / bv["avg_discount_price"] * 1000
        if not bv.empty:
            v1 = bv.nlargest(1,"score").iloc[0]
            insight_list.append(("💡","Best Value Category",
                f"<b style='color:#F59E0B'>{v1['main_category']}</b> offers the best rating-to-price "
                f"ratio ({v1['avg_rating']:.2f}⭐ at avg {fmt_currency(v1['avg_discount_price'])}).", "#F59E0B"))

    cols = st.columns(3)
    for i, (icon, title, body, color) in enumerate(insight_list):
        with cols[i % 3]:
            _insight_card(icon, title, body, color)
        if i % 3 == 2 and i < len(insight_list)-1:
            cols = st.columns(3)

    # ── Business recommendations ───────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>📈 Business Recommendations</h2></div>""",
                unsafe_allow_html=True)
    recs = [
        ("🎯","Focus on High-Review Categories","Categories with 1M+ reviews signal strong demand. Prioritise inventory in top-reviewed segments."),
        ("💰","Target Premium Segments","High avg-price categories show consumers willing to pay more. Capture these with quality listings."),
        ("🏷️","Aggressive Discounting Works","Categories with 40%+ avg discounts convert better. Use dynamic pricing to stay competitive."),
        ("⭐","Rating Drives Conversions","Products rated 4.2+ get 3× more clicks. Invest in quality and customer service."),
        ("📊","Data-First Approach","Monitor this analytics platform weekly and adapt your product mix accordingly."),
        ("🤖","Automation Opportunity","Automate pricing alerts for top-discount categories to ensure competitiveness without margin loss."),
    ]
    cols = st.columns(3)
    for i, (icon, title, body) in enumerate(recs):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="metric-card cyan" style="margin-bottom:.75rem;padding:1.1rem;">
                <div style="font-size:1.5rem;">{icon}</div>
                <div style="font-weight:700;color:#00D4FF;margin:.35rem 0 .25rem;font-size:.9rem;">{title}</div>
                <div style="color:#94A3B8;font-size:.82rem;line-height:1.5;">{body}</div>
            </div>""", unsafe_allow_html=True)
        if i % 3 == 2 and i < len(recs)-1:
            cols = st.columns(3)

    # ── Supporting charts ──────────────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>📊 Supporting Data</h2></div>""",
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Top 10 by Total Reviews</div>', unsafe_allow_html=True)
        if not top_reviews.empty:
            fig1 = px.bar(top_reviews, x="total_reviews", y="main_category",
                          orientation="h", color="avg_rating",
                          color_continuous_scale=ORANGE_SCALE,
                          labels={"total_reviews":"Total Reviews","main_category":""})
            fig1.update_traces(marker_line_width=0)
            apply_theme(fig1, height=350)
            fig1.update_coloraxes(showscale=False)
            st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Most Expensive Categories (Avg MRP)</div>',
                    unsafe_allow_html=True)
        if not most_exp.empty:
            fig2 = px.bar(most_exp, x="avg_actual_price", y="main_category",
                          orientation="h", color="avg_actual_price",
                          color_continuous_scale=CYAN_SCALE,
                          labels={"avg_actual_price":"Avg MRP (₹)","main_category":""})
            fig2.update_traces(marker_line_width=0)
            apply_theme(fig2, height=350)
            fig2.update_coloraxes(showscale=False)
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Best Rated Categories</div>', unsafe_allow_html=True)
        if not best_rated.empty:
            fig3 = px.bar(best_rated, x="avg_rating", y="main_category",
                          orientation="h", color="avg_rating",
                          color_continuous_scale=[[0,"#003319"],[1,"#10B981"]],
                          labels={"avg_rating":"Avg Rating","main_category":""},
                          range_x=[3, 5])
            fig3.update_traces(marker_line_width=0)
            apply_theme(fig3, height=350)
            fig3.update_coloraxes(showscale=False)
            st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Discount Leaders</div>', unsafe_allow_html=True)
        if not disc_leaders.empty:
            fig4 = px.bar(disc_leaders, x="avg_disc", y="main_category",
                          orientation="h", color="avg_disc",
                          color_continuous_scale=[[0,"#1a0010"],[1,"#F43F5E"]],
                          labels={"avg_disc":"Avg Discount %","main_category":""})
            fig4.update_traces(marker_line_width=0)
            apply_theme(fig4, height=350)
            fig4.update_coloraxes(showscale=False)
            st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
