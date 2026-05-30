"""
Download Center – CSV, Excel, PDF exports.
"""
import streamlit as st
import pandas as pd
import io
from datetime import datetime

from utils.db import (get_category_stats, get_top_rated_products,
                      get_cheapest_products, get_most_expensive_products,
                      get_discount_analysis, get_ai_insights, search_products,
                      get_all_categories)
from utils.helpers import to_csv_bytes, to_excel_bytes, fmt_currency, fmt_number


def _pdf_report(title: str, df: pd.DataFrame) -> bytes:
    """Generate a simple PDF report."""
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 12, title, ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 6, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | Amazon Product Analytics", ln=True)
        pdf.ln(4)

        if df.empty:
            pdf.cell(0, 8, "No data available.", ln=True)
        else:
            df_str = df.astype(str)
            cols   = list(df_str.columns)
            # headers
            pdf.set_fill_color(30, 30, 50)
            pdf.set_text_color(255, 153, 0)
            pdf.set_font("Helvetica", "B", 7)
            col_w = min(190 // len(cols), 35)
            for c in cols:
                pdf.cell(col_w, 7, str(c)[:14], border=1, fill=True)
            pdf.ln()
            # rows
            pdf.set_text_color(30, 30, 30)
            pdf.set_font("Helvetica", "", 7)
            for _, row in df_str.head(50).iterrows():
                pdf.set_fill_color(245, 245, 250)
                for c in cols:
                    pdf.cell(col_w, 6, str(row[c])[:14], border=1)
                pdf.ln()

        return pdf.output(dest="S").encode("latin-1")
    except Exception as e:
        # fallback: plain text PDF-like
        content = f"{title}\n{'='*60}\n"
        content += df.to_string(index=False) if not df.empty else "No data."
        return content.encode("utf-8")


def _section(icon: str, title: str, desc: str, df_fn, fn_args=(), fname="report"):
    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:1rem;padding:1.2rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:1rem;">
            <div>
                <div style="font-size:1.4rem;">{icon}</div>
                <div style="font-weight:700;color:var(--text-primary);font-size:.95rem;margin:.3rem 0 .2rem;">{title}</div>
                <div style="color:var(--text-secondary);font-size:.82rem;">{desc}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner(f"Preparing {title}…"):
        df = df_fn(*fn_args) if fn_args else df_fn()

    if df.empty:
        st.warning("No data to export.")
        return

    st.dataframe(df.head(10), use_container_width=True, hide_index=True,
                 height=200)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button(
            f"⬇️ CSV", to_csv_bytes(df),
            file_name=f"{fname}_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv", use_container_width=True,
        )
    with c2:
        st.download_button(
            f"📊 Excel", to_excel_bytes(df),
            file_name=f"{fname}_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with c3:
        st.download_button(
            f"📄 PDF", _pdf_report(title, df),
            file_name=f"{fname}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf", use_container_width=True,
        )
    st.divider()


def render():
    st.markdown("""
    <div class="section-header">
        <h2>⬇️ Download Center</h2>
        <span class="section-badge">3 Formats</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(16,185,129,.08);border:1px solid rgba(16,185,129,.2);
        border-radius:12px;padding:1rem 1.4rem;margin-bottom:1.5rem;">
        <span style="color:var(--accent-4);font-weight:700;">✅ Export any dataset</span>
        <span style="color:var(--text-secondary);font-size:.9rem;margin-left:.5rem;">
        Download as CSV, Excel (XLSX), or PDF Report. All exports include latest live data.
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Custom search export ───────────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>🔍 Custom Export</h2></div>""",
                unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        kw = st.text_input("Search keyword (leave blank for all)", key="dl_kw")
    with c2:
        cats = get_all_categories()
        cat  = st.selectbox("Category", cats, key="dl_cat")

    n_export = st.selectbox("Max rows", [100, 500, 1000, 5000], index=1)

    if st.button("📦 Prepare Custom Export", key="btn_custom_dl"):
        with st.spinner("Fetching data…"):
            df_custom = search_products(kw or "", category=cat, limit=n_export)
        if not df_custom.empty:
            st.success(f"✅ {len(df_custom)} products ready to download")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.download_button("⬇️ CSV",   to_csv_bytes(df_custom),   f"custom_export.csv",  "text/csv", use_container_width=True)
            with c2:
                st.download_button("📊 Excel", to_excel_bytes(df_custom), f"custom_export.xlsx",
                                   "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                   use_container_width=True)
            with c3:
                st.download_button("📄 PDF",   _pdf_report("Custom Export", df_custom),
                                   "custom_export.pdf", "application/pdf", use_container_width=True)

    st.divider()

    # ── Pre-built reports ──────────────────────────────────────────────────────
    st.markdown("""<div class="section-header"><h2>📋 Pre-Built Reports</h2></div>""",
                unsafe_allow_html=True)

    _section("📁", "Category Statistics Report",
             "All categories with product count, avg rating, avg price, reviews & discount %.",
             get_category_stats, fname="category_stats")

    _section("⭐", "Top Rated Products (500+ reviews)",
             "Products rated ≥4.0 with 500+ reviews — sorted by rating.",
             get_top_rated_products, fn_args=(500, 200), fname="top_rated")

    _section("💰", "Cheapest Products",
             "Lowest-priced products on Amazon India.",
             get_cheapest_products, fn_args=(200,), fname="cheapest_products")

    _section("💎", "Most Expensive Products",
             "Premium products with the highest actual prices.",
             get_most_expensive_products, fn_args=(200,), fname="expensive_products")

    _section("🔥", "Discount Analysis by Category",
             "Category-wise average and maximum discount percentages.",
             get_discount_analysis, fname="discount_analysis")
