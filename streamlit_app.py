import streamlit as st
import requests
import pandas as pd

st.title("KapitalIQ - Your Personal Investment Assistant")

base_url = "http://127.0.0.1:8000"#where FASTapi is running

### Dashboard

st.header("Daily Dashboard")

response = requests.get(f"{base_url}/dashboard")
data = response.json()

for ticker, ticker_data in data.items():
    st.subheader(ticker)
    # Stock table
    st.write("**Stock Prices (Last 30 days)**")
    df = pd.DataFrame(ticker_data["stock_data"])
    st.dataframe(df)
    
    # News
    st.write("**Latest News**")
    for article in ticker_data["news"]:
        st.write(f"{article['date']} — {article['source']}")
        st.write(article['content'])
        st.divider()

### Query Section

st.header("Ask KapitalIQ")

user_query = st.text_input("Ask a question about DAX stocks:")

if st.button("Analyze"):
    if user_query:
        with st.spinner("Analyzing..."):
            response = requests.post(
                f"{base_url}/query",
                json={"query": user_query}
            )
            result = response.json()
            st.write("**Assistant Response:**")
            st.write(result["Assistant Response"])
    else:
        st.warning("Please enter a question.")