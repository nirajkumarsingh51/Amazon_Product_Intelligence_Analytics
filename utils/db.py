"""
Database connection and query utilities.
Prices in amazon_products are stored as VARCHAR like "₹1,299" — we CAST them
via REGEXP_REPLACE so all numeric operations work correctly.
"""
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import logging
import re

logger = logging.getLogger(__name__)
DB_URL = "mysql+pymysql://root:pk252914@localhost:3306/amazon_cleaning_db"

# ── Price-cleaning SQL expression ─────────────────────────────────────────────
# Strips "₹", "," and whitespace then casts to DECIMAL
def _price_expr(col: str) -> str:
    """Return SQL that converts a messy price string column to DECIMAL."""
    return (f"CAST(REPLACE(REPLACE(REPLACE(REPLACE({col},'₹',''),',',' '),' ',''),'\u20b9','') "
            f"AS DECIMAL(15,2))")

# Pre-built expressions for the two main price columns
DISC  = _price_expr("discount_price")
ACT   = _price_expr("actual_price")


@st.cache_resource(show_spinner=False)
def get_engine():
    try:
        engine = create_engine(DB_URL, pool_size=5, max_overflow=10,
                               pool_pre_ping=True, pool_recycle=3600)
        return engine
    except Exception as e:
        logger.error(f"Engine creation failed: {e}")
        return None


def run_query(sql: str, params: dict = None) -> pd.DataFrame:
    engine = get_engine()
    if engine is None:
        return pd.DataFrame()
    try:
        with engine.connect() as conn:
            return pd.read_sql(text(sql), conn, params=params)
    except Exception as e:
        logger.error(f"Query error: {e}\nSQL: {sql}")
        return pd.DataFrame()


# ── Detect whether prices are already numeric or need cleaning ─────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def _prices_are_numeric() -> bool:
    """Returns True if discount_price column is already a numeric type."""
    df = run_query(
        "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA='amazon_cleaning_db' AND TABLE_NAME='amazon_products' "
        "AND COLUMN_NAME='discount_price' LIMIT 1"
    )
    if df.empty:
        return False
    dtype = str(df.iloc[0, 0]).lower()
    return dtype in ("decimal","float","double","int","bigint","numeric")


def _dp() -> str:
    """Return the correct SQL expression for discount_price."""
    return "discount_price" if _prices_are_numeric() else DISC


def _ap() -> str:
    """Return the correct SQL expression for actual_price."""
    return "actual_price" if _prices_are_numeric() else ACT


# ── KPIs ───────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def get_executive_kpis() -> dict:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT
            COUNT(*)                                                AS total_products,
            COUNT(DISTINCT main_category)                           AS total_categories,
            COUNT(DISTINCT sub_category)                            AS total_sub_categories,
            ROUND(AVG(ratings), 2)                                  AS avg_rating,
            ROUND(AVG({dp}), 2)                                     AS avg_discount_price,
            ROUND(AVG({ap}), 2)                                     AS avg_actual_price,
            SUM(no_of_ratings)                                      AS total_reviews,
            ROUND(AVG(({ap} - {dp}) / NULLIF({ap}, 0) * 100), 1)   AS avg_discount_pct
        FROM amazon_products
        WHERE {ap} IS NOT NULL AND {ap} > 0
    """
    df = run_query(sql)
    return {} if df.empty else df.iloc[0].to_dict()


@st.cache_data(ttl=600, show_spinner=False)
def get_category_stats() -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT
            main_category,
            COUNT(*)                                                        AS product_count,
            ROUND(AVG(ratings), 2)                                          AS avg_rating,
            ROUND(AVG({dp}), 2)                                             AS avg_discount_price,
            ROUND(AVG({ap}), 2)                                             AS avg_actual_price,
            SUM(no_of_ratings)                                              AS total_reviews,
            ROUND(AVG(({ap} - {dp}) / NULLIF({ap}, 0) * 100), 1)           AS avg_discount_pct
        FROM amazon_products
        WHERE main_category IS NOT NULL AND main_category != ''
        GROUP BY main_category
        ORDER BY product_count DESC
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_sub_category_stats(main_category: str = None) -> pd.DataFrame:
    dp = _dp()
    if main_category and main_category != "All":
        sql = f"""
            SELECT sub_category, main_category,
                COUNT(*) AS product_count,
                ROUND(AVG(ratings), 2) AS avg_rating,
                ROUND(AVG({dp}), 2) AS avg_discount_price
            FROM amazon_products
            WHERE main_category = :cat AND sub_category IS NOT NULL AND sub_category != ''
            GROUP BY sub_category, main_category
            ORDER BY product_count DESC LIMIT 30
        """
        return run_query(sql, {"cat": main_category})
    sql = f"""
        SELECT sub_category, main_category,
            COUNT(*) AS product_count,
            ROUND(AVG(ratings), 2) AS avg_rating,
            ROUND(AVG({dp}), 2) AS avg_discount_price
        FROM amazon_products
        WHERE sub_category IS NOT NULL AND sub_category != ''
        GROUP BY sub_category, main_category
        ORDER BY product_count DESC LIMIT 40
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_price_distribution() -> pd.DataFrame:
    dp = _dp()
    sql = f"""
        SELECT {dp} AS discount_price
        FROM amazon_products
        WHERE {dp} IS NOT NULL AND {dp} > 0 AND {dp} < 50000
        LIMIT 50000
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_cheapest_products(limit: int = 20) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE {dp} IS NOT NULL AND {dp} > 0
          AND name IS NOT NULL AND name != ''
        ORDER BY {dp} ASC
        LIMIT :lim
    """
    return run_query(sql, {"lim": limit})


@st.cache_data(ttl=600, show_spinner=False)
def get_most_expensive_products(limit: int = 20) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE {ap} IS NOT NULL AND {ap} > 0
          AND name IS NOT NULL AND name != ''
        ORDER BY {ap} DESC
        LIMIT :lim
    """
    return run_query(sql, {"lim": limit})


@st.cache_data(ttl=600, show_spinner=False)
def get_top_rated_products(min_reviews: int = 500, limit: int = 20) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE ratings IS NOT NULL AND ratings >= 4.0
          AND no_of_ratings >= :min_rev
          AND name IS NOT NULL AND name != ''
        ORDER BY ratings DESC, no_of_ratings DESC
        LIMIT :lim
    """
    return run_query(sql, {"min_rev": min_reviews, "lim": limit})


@st.cache_data(ttl=600, show_spinner=False)
def get_rating_distribution() -> pd.DataFrame:
    sql = """
        SELECT ROUND(ratings, 1) AS rating_bucket, COUNT(*) AS count
        FROM amazon_products
        WHERE ratings IS NOT NULL AND ratings > 0
        GROUP BY rating_bucket ORDER BY rating_bucket
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_rating_vs_price(sample: int = 5000) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT ratings, {dp} AS discount_price, {ap} AS actual_price,
               main_category, no_of_ratings
        FROM amazon_products
        WHERE ratings IS NOT NULL AND {dp} IS NOT NULL
          AND {dp} > 0 AND {dp} < 100000 AND ratings > 0
        ORDER BY RAND()
        LIMIT :s
    """
    return run_query(sql, {"s": sample})


@st.cache_data(ttl=300, show_spinner=False)
def search_products(query: str, category: str = "All",
                    min_rating: float = 0.0, max_price: float = 1_000_000,
                    limit: int = 50) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    base = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE name LIKE :q
          AND (ratings >= :min_rat OR ratings IS NULL)
          AND ({dp} <= :max_p OR {dp} IS NULL)
    """
    params = {"q": f"%{query}%", "min_rat": min_rating, "max_p": max_price, "lim": limit}
    if category and category != "All":
        base += " AND main_category = :cat"
        params["cat"] = category
    base += " ORDER BY no_of_ratings DESC LIMIT :lim"
    return run_query(base, params)


@st.cache_data(ttl=600, show_spinner=False)
def get_all_categories() -> list:
    df = run_query(
        "SELECT DISTINCT main_category FROM amazon_products "
        "WHERE main_category IS NOT NULL AND main_category != '' "
        "ORDER BY main_category"
    )
    return ["All"] + df["main_category"].tolist() if not df.empty else ["All"]


@st.cache_data(ttl=600, show_spinner=False)
def get_discount_analysis() -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT main_category,
            ROUND(AVG(({ap} - {dp}) / NULLIF({ap}, 0) * 100), 1) AS avg_discount_pct,
            ROUND(MAX(({ap} - {dp}) / NULLIF({ap}, 0) * 100), 1) AS max_discount_pct,
            COUNT(*) AS product_count
        FROM amazon_products
        WHERE {ap} > 0 AND {dp} > 0 AND {ap} >= {dp}
        GROUP BY main_category
        ORDER BY avg_discount_pct DESC
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_heatmap_data() -> pd.DataFrame:
    dp = _dp()
    sql = f"""
        SELECT main_category,
               FLOOR({dp}/1000)*1000 AS price_bucket,
               ROUND(AVG(ratings), 2) AS avg_rating,
               COUNT(*) AS product_count
        FROM amazon_products
        WHERE {dp} IS NOT NULL AND {dp} > 0 AND {dp} < 50000
          AND ratings IS NOT NULL
          AND main_category IS NOT NULL AND main_category != ''
        GROUP BY main_category, price_bucket
        ORDER BY main_category, price_bucket
    """
    return run_query(sql)


@st.cache_data(ttl=600, show_spinner=False)
def get_recommendations(category: str, limit: int = 12) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    sql = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE main_category = :cat
          AND ratings IS NOT NULL AND ratings >= 3.5
          AND no_of_ratings IS NOT NULL AND no_of_ratings > 50
          AND name IS NOT NULL AND image IS NOT NULL
        ORDER BY (ratings * LOG(no_of_ratings + 1)) DESC
        LIMIT :lim
    """
    return run_query(sql, {"cat": category, "lim": limit})


@st.cache_data(ttl=600, show_spinner=False)
def get_gallery_products(category: str = "All", limit: int = 24) -> pd.DataFrame:
    dp = _dp(); ap = _ap()
    if category != "All":
        sql = f"""
            SELECT name, main_category, sub_category, ratings, no_of_ratings,
                   {dp} AS discount_price, {ap} AS actual_price, image, link
            FROM amazon_products
            WHERE main_category = :cat AND image IS NOT NULL AND image != ''
              AND name IS NOT NULL
            ORDER BY no_of_ratings DESC LIMIT :lim
        """
        return run_query(sql, {"cat": category, "lim": limit})
    sql = f"""
        SELECT name, main_category, sub_category, ratings, no_of_ratings,
               {dp} AS discount_price, {ap} AS actual_price, image, link
        FROM amazon_products
        WHERE image IS NOT NULL AND image != '' AND name IS NOT NULL
        ORDER BY no_of_ratings DESC LIMIT :lim
    """
    return run_query(sql, {"lim": limit})


@st.cache_data(ttl=600, show_spinner=False)
def get_ai_insights() -> dict:
    dp = _dp(); ap = _ap()
    top_cats = run_query(f"""
        SELECT main_category, COUNT(*) AS products,
               ROUND(AVG(ratings),2) AS avg_rating,
               ROUND(AVG({dp}),2) AS avg_price,
               SUM(no_of_ratings) AS total_reviews
        FROM amazon_products WHERE main_category IS NOT NULL AND main_category != ''
        GROUP BY main_category ORDER BY total_reviews DESC LIMIT 10
    """)
    expensive_cats = run_query(f"""
        SELECT main_category, ROUND(AVG({ap}),2) AS avg_actual_price
        FROM amazon_products WHERE {ap} > 0 AND main_category IS NOT NULL
        GROUP BY main_category ORDER BY avg_actual_price DESC LIMIT 10
    """)
    best_rated_cats = run_query(f"""
        SELECT main_category, ROUND(AVG(ratings),2) AS avg_rating, COUNT(*) AS products
        FROM amazon_products WHERE ratings > 0 AND main_category IS NOT NULL
        GROUP BY main_category HAVING products > 100
        ORDER BY avg_rating DESC LIMIT 10
    """)
    discount_leaders = run_query(f"""
        SELECT main_category,
            ROUND(AVG(({ap}-{dp})/NULLIF({ap},0)*100),1) AS avg_disc
        FROM amazon_products
        WHERE {ap} > 0 AND {dp} > 0 AND {ap} >= {dp}
        GROUP BY main_category ORDER BY avg_disc DESC LIMIT 10
    """)
    return {
        "top_by_reviews": top_cats,
        "most_expensive": expensive_cats,
        "best_rated": best_rated_cats,
        "discount_leaders": discount_leaders,
    }
