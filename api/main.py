from fastapi import FastAPI
from pipelines.database import SessionLocal
from pipelines.models import StockPrice, NewsArticle
from sqlalchemy import select, desc
from datetime import date, timedelta
from pydantic import BaseModel
from agents.intent_router import IntentRouter
from pipelines.on_demand_fetcher import fetch_on_demand
from pipelines.stock_fetcher import StockFetcher
from pipelines.data_cleaner import DataCleaner
from agents.orchestrator import app as orchestrator_app

app = FastAPI(title="KapitalIQ", version="1.0")

#a deocrator for when someone sends a GET request to /health, run this function
@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/dashboard")
def get_dashboard():
    db = SessionLocal()
    tickers = ["SAP.DE", "SIE.DE", "DTE.DE", "ALV.DE", "AIR.DE"]
    result = {}
    
    try:
        for ticker in tickers:
            
            # Stock query — last 30 days
            stock_rows = db.execute(
                select(StockPrice)
                .where(StockPrice.ticker == ticker)
                .order_by(desc(StockPrice.date))
                .limit(30)
            ).scalars().all()
            
            # Convert to list of dicts
            stock_data = [
                {"date": str(row.date), "close": row.close, "volume": row.volume}
                for row in stock_rows
            ]
            
            # News query — last 3 articles
            news_rows = db.execute(
                select(NewsArticle)
                .where(NewsArticle.ticker == ticker)
                .order_by(desc(NewsArticle.published_date))
                .limit(3)
            ).scalars().all()
            
            # Convert to list of dicts
            news_data = [
                {"date": str(row.published_date), "source": row.news_source, "content": row.chunk_text}
                for row in news_rows
            ]
            
            result[ticker] = {
                "stock_data": stock_data,
                "news": news_data
            }
        return result
    finally:
        db.close()

#to let FASTapi know the data and its type. without basemodel(from pydantic) the validation of every field is manual
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
def handle_query(request: QueryRequest):
    router = IntentRouter()
    intent, ticker = router.run(request.query)
    #return {"intent": intent, "ticker": ticker}

    if intent == "GENERAL":
    # return a general answer without orchestrator
        return {"intent": intent, "ticker": None, "decision": "Please ask a stock specific question."}
    
    elif intent in ["DASHBOARD", "ON_DEMAND"]:
        if intent == "ON_DEMAND":
            fetch_on_demand(ticker)

        fetcher = StockFetcher(ticker)
        data = fetcher.fetch()

        cleaner = DataCleaner(data)
        clean_data = cleaner.clean()

        response = orchestrator_app.invoke({ 
        "ticker": ticker,
        "user_query": request.query,
        "cleaned_data": clean_data,
        "analysis_result": "",
        "nlp_result": "",
        "final_decision": ""

         }) 
        #removing the "intent" to not confuse the user. as the intent needs to be worked on
        #return {"intent": intent, "ticker": ticker, "decision": response["final_decision"]}
        return {"ticker": ticker, "Assistant Response": response["final_decision"]}
        
    
    