"""
Utility helpers: formatting, exports, styling.
"""
import io
import pandas as pd


def fmt_currency(val):
    """Format a number as Indian Rupee."""
    if val is None or (isinstance(val, float) and val != val):
        return "N/A"
    try:
        return f"₹{float(val):,.0f}"
    except Exception:
        return "N/A"


def fmt_number(val):
    if val is None:
        return "N/A"
    try:
        v = float(val)
        if v >= 1_000_000:
            return f"{v/1_000_000:.1f}M"
        if v >= 1_000:
            return f"{v/1_000:.1f}K"
        return f"{v:,.0f}"
    except Exception:
        return "N/A"


def fmt_rating(val):
    if val is None:
        return "N/A"
    try:
        stars = "⭐" * int(round(float(val)))
        return f"{float(val):.1f} {stars}"
    except Exception:
        return "N/A"


def rating_stars(val, max_val: float = 5.0) -> str:
    """Return filled/empty star string."""
    try:
        v = float(val)
        filled = round(v)
        empty = round(max_val) - filled
        return "★" * filled + "☆" * empty
    except Exception:
        return "☆☆☆☆☆"


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return buf.getvalue()


def truncate(text: str, n: int = 60) -> str:
    if not text:
        return ""
    return text[:n] + "…" if len(text) > n else text


CATEGORY_ICONS = {
    "shirts": "👔",
    "watches": "⌚",
    "air_conditioners": "❄️",
    "sports_shoes": "👟",
    "jeans": "👖",
    "western_wear": "👗",
    "home_furnishing": "🛋️",
    "electronics": "💻",
    "televisions": "📺",
    "refrigerators": "🧊",
    "cameras": "📷",
    "headphones": "🎧",
    "jewellery": "💍",
    "shoes": "👠",
    "bags_and_luggage": "🧳",
    "toys_and_games": "🧸",
    "kitchen_and_dining": "🍳",
    "beauty_and_grooming": "💄",
    "furniture": "🪑",
    "books": "📚",
    "sports": "⚽",
    "cycling": "🚴",
    "cricket": "🏏",
    "yoga": "🧘",
    "running": "🏃",
    "football": "⚽",
    "badminton": "🏸",
    "car_accessories": "🚗",
    "baby_products": "👶",
    "dog_supplies": "🐶",
    "pet_supplies": "🐾",
    "garden": "🌿",
    "speakers": "🔊",
    "mobile": "📱",
    "laptop": "💻",
    "default": "🛒",
}


def get_category_icon(category: str) -> str:
    if not category:
        return CATEGORY_ICONS["default"]
    cat_lower = category.lower().replace(" ", "_")
    for key, icon in CATEGORY_ICONS.items():
        if key in cat_lower:
            return icon
    return CATEGORY_ICONS["default"]
