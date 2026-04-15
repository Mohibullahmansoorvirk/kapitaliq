import streamlit as st
import os

import requests
import pandas as pd

st.title("KapitalIQ - Your Personal Investment Assistant")

#base_url = "http://127.0.0.1:8000"#originally where FastAPI is running

#base_url = "http://fastapi:8000" #for docker container - local deployment "fastapi" the service name in docker-compose.yml
base_url = os.getenv("FASTAPI_URL", "http://localhost:8000") # for Railway cloud deployment
### Dashboard

st.header("Daily Dashboard")
# Fetch dashboard data from FastAPI
response = requests.get(f"{base_url}/dashboard")
data = response.json()
# Loop over each ticker and display stocks data & news
for ticker, ticker_data in data.items():
    st.subheader(ticker)
    # Stock prices table
    st.write("**Stock Prices (Last 30 days)**")
    df = pd.DataFrame(ticker_data["stock_data"])
    st.dataframe(df)
    
    # Latest News Articles
    st.write("**Latest News**")
    for article in ticker_data["news"]:
        st.write(f"{article['date']} — {article['source']}")
        st.write(article['content'])
        st.divider()

### Query Section (at the bottom)

st.header("Ask KapitalIQ")

user_query = st.text_input("Ask a question about DAX stocks:")

if st.button("Analyze"):
    if user_query:
        #Send query to FastAPI and display the decision from orchestrator
        with st.spinner("Analyzing..."):
            response = requests.post(
                f"{base_url}/query",
                json={"query": user_query}
            )
            result = response.json()
            st.write("**Assistant Response:**")
            st.write(result["Assistant_Response"])
    else:
        st.warning("Please enter a question.")