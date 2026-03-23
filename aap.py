import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI IPO Analyzer", layout="wide")

st.title("📊 AI IPO Analysis & Recommendation System (India)")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.header("🔍 Enter IPO Details")

ipo_name = st.text_input("IPO Name")

price_band = st.number_input("Price Band (₹)", min_value=1)
gmp = st.number_input("Grey Market Premium (₹)", min_value=0)

revenue_growth = st.slider("Revenue Growth (%)", 0, 100, 20)
profit_margin = st.slider("Profit Margin (%)", 0, 50, 15)
roe = st.slider("ROE (%)", 0, 50, 15)

pe_ratio = st.number_input("IPO P/E Ratio", min_value=1.0)
peer_pe = st.number_input("Industry P/E (Peer Avg)", min_value=1.0)

# -----------------------------
# ANALYSIS LOGIC
# -----------------------------
def calculate_scores():
    
    # Financial Score (out of 10)
    financial_score = (revenue_growth * 0.3 + profit_margin * 0.3 + roe * 0.4) / 10

    # Valuation Score (out of 10)
    if pe_ratio <= peer_pe:
        valuation_score = 8
    elif pe_ratio <= peer_pe * 1.2:
        valuation_score = 6
    else:
        valuation_score = 4

    # GMP Sentiment Score (out of 10)
    if gmp > 100:
        sentiment_score = 9
    elif gmp > 50:
        sentiment_score = 7
    elif gmp > 0:
        sentiment_score = 5
    else:
        sentiment_score = 3

    # Final IPO Score
    ipo_score = round((financial_score + valuation_score + sentiment_score) / 3, 2)

    # Listing Gain Probability
    if gmp > 100:
        listing_prob = "High (70-90%)"
    elif gmp > 50:
        listing_prob = "Moderate (50-70%)"
    elif gmp > 0:
        listing_prob = "Low (30-50%)"
    else:
        listing_prob = "Very Low (<30%)"

    # Final Recommendation
    if ipo_score >= 7:
        recommendation = "🟢 INVEST (Strong Fundamentals)"
    elif ipo_score >= 5:
        recommendation = "🟡 APPLY FOR LISTING GAINS"
    else:
        recommendation = "🔴 AVOID"

    return financial_score, valuation_score, sentiment_score, ipo_score, listing_prob, recommendation


# -----------------------------
# OUTPUT SECTION
# -----------------------------
if st.button("🚀 Analyze IPO"):

    (financial_score, valuation_score, sentiment_score,
     ipo_score, listing_prob, recommendation) = calculate_scores()

    st.header(f"📊 Analysis Result for {ipo_name}")

    col1, col2, col3 = st.columns(3)

    col1.metric("📈 Financial Score", f"{round(financial_score,2)}/10")
    col2.metric("💰 Valuation Score", f"{valuation_score}/10")
    col3.metric("📊 Sentiment Score (GMP)", f"{sentiment_score}/10")

    st.subheader("⭐ Final IPO Score")
    st.success(f"{ipo_score} / 10")

    st.subheader("📉 Listing Gain Probability")
    st.info(listing_prob)

    st.subheader("🤖 Final Recommendation")
    st.warning(recommendation)

    # Insights
    st.subheader("🧠 Key Insights")

    insights = []

    if revenue_growth > 20:
        insights.append("Strong revenue growth")
    else:
        insights.append("Moderate revenue growth")

    if pe_ratio > peer_pe:
        insights.append("Overvalued compared to peers")
    else:
        insights.append("Fair valuation")

    if gmp > 50:
        insights.append("High market demand (positive sentiment)")
    else:
        insights.append("Weak market sentiment")

    for i in insights:
        st.write(f"- {i}")
