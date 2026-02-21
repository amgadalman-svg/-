# full_investment_advisor_he.py
import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="יועץ השקעות אישי", layout="wide")
st.markdown("<h1 style='text-align: right;'>🧠 יועץ השקעות אישי — גרסה מלאה</h1>", unsafe_allow_html=True)

# ------------------------------
# 1️⃣ בחירת מודולים
st.header("שלב 1 – בחר מודולי V")
v_modules = st.multiselect(
    "בחר מודולים:",
    ["V1 – יועץ בסיסי",
     "V2 – ניתוח תיק",
     "V3 – מצב מאקרו",
     "V4 – פסיכולוגיה למשקיע",
     "V5 – שכבת ביצוע",
     "V6 – למידה אסטרטגית",
     "V7 – הקצאת הון חכמה",
     "V8 – ניהול מחזור חיים של עושר"]
)

# ------------------------------
# 2️⃣ בחירת סוג סקירה
st.header("שלב 2 – סוג סקירה")
report_type = st.radio(
    "בחר תדירות סקירה:",
    ["יומית", "שבועית", "חודשית", "רבעונית", "שנתית"]
)

# ------------------------------
# 3️⃣ סיכום תיק
st.header("שלב 3 – סיכום תיק")
summary_type = st.radio(
    "סיכום תיק:",
    ["ללא", "חודשי", "רבעוני", "שנתי"]
)

# ------------------------------
# 4️⃣ בדיקה של נכסים חדשים
st.header("שלב 4 – בדיקת מניות / ETF חדשים")
new_assets_input = st.text_input("הכנס סמלים מופרדים בפסיק (לדוגמה: AAPL, MSFT, EEM):")
new_assets = [a.strip().upper() for a in new_assets_input.split(",") if a.strip()]

# ------------------------------
# 5️⃣ הגדרת תיק בסיסי
portfolio = {
    "IVV": 0.30,        # Invesco S&P 500 ETF
    "IEUR": 0.15,       # MSCI Europe ETF
    "EEM": 0.15,        # MSCI EM ETF
    "USSC LN": 0.15,    # Small Cap Value US
    "ZPRX": 0.05,       # Small Cap Value Euro
    "TA-90": 0.10,
    "TA-35": 0.05,
    "APP": 0.025,       # AppLovin
    "PONY": 0.025       # Pony AI
}

# ------------------------------
# פונקציות עזר
def get_price(symbol):
    try:
        data = yf.Ticker(symbol)
        return data.history(period="1d")['Close'][-1]
    except:
        return np.nan

def get_historical_prices(symbol, period="3y"):
    try:
        data = yf.Ticker(symbol)
        df = data.history(period=period)
        return df['Close']
    except:
        return pd.Series(dtype=float)

def calculate_cagr(prices):
    if len(prices) < 2:
        return np.nan
    start_price = prices[0]
    end_price = prices[-1]
    n_years = (prices.index[-1] - prices.index[0]).days / 365.25
    return (end_price / start_price) ** (1 / n_years) - 1

def calculate_drawdown(prices):
    cumulative = prices / prices[0]
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

# ------------------------------
# הצגת מחירי תיק נוכחי
st.subheader("📊 מחירי תיק נוכחי")
portfolio_df = pd.DataFrame(portfolio.items(), columns=["נכס", "משקל"])
portfolio_df["מחיר"] = portfolio_df["נכס"].apply(get_price)
st.dataframe(portfolio_df)

# ------------------------------
# What-If ניתוח נכסים חדשים
if new_assets:
    st.subheader("➕ ניתוח נכסים חדשים")
    new_assets_prices = {a: get_price(a) for a in new_assets}
    new_assets_df = pd.DataFrame(list(new_assets_prices.items()), columns=["נכס", "מחיר"])
    st.dataframe(new_assets_df)

    total_existing = sum(portfolio.values())
    new_weight = (1 - total_existing) / len(new_assets) if len(new_assets) > 0 else 0
    for asset in new_assets:
        portfolio[asset] = new_weight
    adjusted_df = pd.DataFrame(portfolio.items(), columns=["נכס", "משקל"])
    st.markdown("**תיק לאחר הוספת נכסים חדשים:**")
    st.dataframe(adjusted_df)

# ------------------------------
# חישובי CAGR ו-Drawdown
st.subheader("📈 ביצועי תיק (CAGR ו-Drawdown)")
performance_data = []
for asset in portfolio.keys():
    prices = get_historical_prices(asset)
    cagr = calculate_cagr(prices)
    drawdown = calculate_drawdown(prices)
    performance_data.append([asset, round(cagr*100,2), round(drawdown*100,2)])
perf_df = pd.DataFrame(performance_data, columns=["נכס", "CAGR (%)", "Drawdown מקסימלי (%)"])
st.dataframe(perf_df)

# ------------------------------
# שורה תחתונה
st.subheader("🧾 מסקנה")
st.success("🟢 התיק יציב, האסטרטגיה לטווח ארוך מתואמת. (Placeholder לניתוח AI חכם)")

# ------------------------------
# מבט קדימה
st.subheader("🔮 מבט קדימה / אירועים קרובים")
st.markdown("- מעקב אחרי ריבית, דוחות רבעוניים ומאקרו.\n- התרעות Rebalance במקרה של חריגות משקל.\n- בדיקת נכסים פוטנציאליים להרחבת רכיב Alpha.")

# ------------------------------
# שמירת snapshot תיק
if st.button("💾 שמור snapshot תיק"):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    portfolio_df.to_csv(f"portfolio_snapshot_{now}.csv", index=False)
    st.success(f"Snapshot של התיק נשמר כ-portfolio_snapshot_{now}.csv")