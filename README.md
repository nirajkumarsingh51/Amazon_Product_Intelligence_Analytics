# 🛒 Amazon Product Intelligence & Analytics Platform

> Enterprise-grade Streamlit analytics dashboard for 551,585+ Amazon India products.

---

## 🚀 Quick Start

```bash
# 1. Clone / extract the project
cd amazon-product-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Ensure MySQL is running with amazon_cleaning_db
#    Connection: mysql+pymysql://root:pk252914@localhost:3306/amazon_cleaning_db

# 4. Launch
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
amazon-product-analytics/
├── app.py                          # Main entry point
├── requirements.txt
├── README.md
├── dashboard/
│   ├── executive.py                # KPI overview
│   ├── search.py                   # Product search engine
│   ├── category.py                 # Category analytics
│   ├── price.py                    # Price intelligence
│   ├── ratings.py                  # Rating analytics
│   ├── recommendations.py          # Recommendation system
│   ├── visual_analytics.py         # Advanced charts (7 types)
│   ├── gallery.py                  # Product image gallery
│   ├── ai_insights.py              # AI-generated insights
│   └── downloads.py                # CSV / Excel / PDF exports
├── utils/
│   ├── db.py                       # All DB queries + caching
│   ├── helpers.py                  # Formatting & utilities
│   └── styles.py                   # Global CSS + Plotly theme
├── assets/                         # Static files
└── reports/                        # Generated reports
```

---

## ✨ Features

| Module | Features |
|--------|----------|
| 🏠 Executive Dashboard | 8 KPI cards, top-category bar + pie, rating distribution, discount analysis |
| 🔍 Search Engine | Keyword search, category + price + rating filters, card + table views |
| 📁 Category Analytics | Treemap, sunburst, bubble chart, sub-category drill-down, category grid |
| 💰 Price Intelligence | Price histogram, category price comparison, discount % charts, cheapest/expensive tables |
| ⭐ Rating Intelligence | Rating distribution, category ratings, scatter plot, top-rated product grid |
| 🤖 Recommendations | Category-based, rating-based, similar-products (3 tabs) |
| 📊 Visual Analytics | Heatmap, treemap, bubble, sunburst, scatter+marginals, histogram, seaborn |
| 🖼️ Gallery | Amazon-style image grid with discount badges and direct product links |
| 🧠 AI Insights | Auto-generated market analysis, business recommendations, 4 supporting charts |
| ⬇️ Downloads | CSV, Excel, PDF for 5 pre-built reports + custom filtered export |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit 1.35** — UI framework
- **SQLAlchemy + PyMySQL** — MySQL connectivity
- **Pandas + NumPy** — Data processing
- **Plotly** — Interactive charts
- **Matplotlib + Seaborn** — Static charts
- **scikit-learn** — ML utilities
- **fpdf2** — PDF generation
- **openpyxl** — Excel export

---

## ⚙️ Database

- **Host:** localhost:3306
- **Database:** `amazon_cleaning_db`
- **Main table:** `amazon_products` (551,585+ rows)
- **Additional:** 113 category-specific tables

---

## 🎨 Design

- Dark theme with glassmorphism cards
- Amazon orange (#FF9900) + Cyan (#00D4FF) accent palette
- Animated metric cards with color-coded top borders
- Full Plotly interactive charts with custom dark theme
- Mobile-responsive sidebar navigation

---

*Built for portfolio & interview showcase. Production-ready architecture.*
