### KapitalIQ

- AI powered Investment Analyst for German DAX stocks. Built as a production grade Multi-Agent System.

- Live Demo: https://web-production-99ef9.up.railway.app/

- API Docs: https://kapitaliq-production.up.railway.app/docs


### The Problem Statement

- A retail investor tracking DAX stocks today opens multiple browser tabs, reads multiple news sites, manually compares price trends and still makes a gut decision. 

- KapitalIQ replaces that workflow. Every morning at 9:30am shortly after the DAX market opens, the system automatically fetches fresh prices and news.

- Runs them through specialized AI agents, resolves conflicts between agents and delivers a single explainable investment signal per stock.


### Architecture



### Key Design Decisions

1. LangGraph over a simple chain because:

- Each agent owns typed state, retries are handled at node level and the flow is explicit and testable. 

- A chain is a black box. A graph is an architecture.

2. Financial signal based reasoning over price forecasting because:

- LSTM and ARIMA produce a number with no explanation. Signal based reasoning with an LLM produces a direction, supporting evidence and a recommendation.

- Defensible and traceable in a real production environment.

3. A dedicated FinalDecisionAgent because:

- Hardcoding "always trust price data over news" results in a bias. An LLM arbitrator reads both arguments and picks the stronger one dynamically.

- Mimicking how a real analyst thinks.

4. An IntentRouter because:

- Without a router, every query hits the full agent pipeline which is expensive and slow. 

- The Intent Router classifies the query first and routes it to the right handler. 

- "GENERAL" queries never touch the orchestrator. 

- "DASHBOARD" queries skip the data fetch. 

- "Only ON_DEMAND" queries run the full pipeline.


### Tech Stack
| Layer | Technology | Version |
|---|---|---|
| Orchestration | LangGraph | Alpha |
| LLM | Groq - LLaMA 3.3 70B | Alpha |
| LLM Framework | LangChain | Alpha |
| Embeddings | HuggingFace - all-mpnet-base-v2 | Alpha |
| Vector Store | PostgreSQL + pgvector | Alpha |
| Object Relation Mapping + Migrations | SQLAlchemy + Alembic | Alpha |
| API | FastAPI | Alpha |
| Frontend | Streamlit | Alpha |
| Scheduling | APScheduler | Alpha |
| Data Sources | yfinance + NewsAPI | Alpha |
| Local Deployment | Dockers | Alpha |
| Cloud Deployment | Railway | Alpha |
| CI/CD | GitHub Actions | Alpha |
| Language | Python 3.13 | Alpha |
| LLM Monitoring | Langfuse | Beta |
| Authentication | JWT via FastAPI | Beta |
| News Data | Finnhub or Polygon.io | Beta |
| Caching | Redis | Gamma |
| Task Queue | Celery + RabbitMQ | Gamma |
| Container Orchestration | Kubernetes | Gamma |
| Price Streaming | WebSocket - Alpaca or IB | Gamma |
| Cloud | AWS multi-region | Gamma |


## Project Structure

```
kapitaliq/
├── agents/
│   ├── data_analysis_agent.py    # Indicators + LLM narrative
│   ├── nlp_agent.py              # RAG retrieval + sentiment
│   ├── final_decision_agent.py   # LLM arbitrator
│   ├── intent_router.py          # Query classifier
│   └── orchestrator.py           # LangGraph StateGraph
├── pipelines/
│   ├── stock_fetcher.py          # yfinance with error handling
│   ├── data_cleaner.py           # OHLCV cleaning
│   ├── data_storage.py           # UPSERT to PostgreSQL
│   ├── news_fetcher.py           # NewsAPI per ticker
│   ├── chunker.py                # 300-word chunks, 45-word overlap
│   ├── embedder.py               # HuggingFace embeddings
│   ├── news_storage.py           # Chunk + embed + store
│   ├── rag_retriever.py          # Cosine similarity + metadata filter
│   ├── on_demand_fetcher.py      # Fresh fetch on user query
│   ├── scheduler.py              # APScheduler jobs
│   ├── models.py                 # SQLAlchemy ORM models
│   └── database.py               # Engine + SessionLocal
├── api/main.py                   # FastAPI — /health /dashboard /query
├── configs/agents.py             # Centralized config
├── tests/                        # 21 unit tests, all passing
├── alembic/                      # Migration history
├── streamlit_app.py              # Dashboard
├── startup.py                    # pgvector + migrations on boot
└── docker-compose.yml            # Local development
```

---

### Project Roadmap

- KapitalIQ is built in three phases:
1. Alpha: A working MVP

2. Beta: To bring it in a form which is ready for initial user testing

3. Gamma: To make it ready for public production use


| Version | Status | Completion Date |
|---|---|---|
| Alpha | Complete | 25.04.2026 |
| Beta | In Progress | 31.07.2026 |
| Gamma | Planned | 31.10.2026 |

### Alpha

- MVP delivered and shipped.

- Data pipeline | RAG | multi-agent orchestration | FastAPI | Streamlit dashboard | Docker | cloud deployment | CI/CD

### Beta

- In Progress

- Structured logging sweep across all modules

- Langfuse Monitoring - LLM call tracing and cost monitoring

- JWT authentication on API endpoints

- Input sanitization and prompt injection detection (one attack vector)

- Integration test suite

- Multi stock query support

- Conversational response format for open ended queries

- Switch from NewsAPI free tier to Finnhub and/or Polygon.io

- Streamlit UI polish

### Gamma

- Planned for full public production readiness 

- Kubernetes | Redis caching | async task queues | real time price streaming | AWS multi region deployment | user accounts 

- Watchlists | push alerts |exportable reports | GDPR & EU compliance | role-based access control | full DAX 40 coverage | Security implementation


### Author

Built by Mohibullah Mansoor Virk - AI Engineer, Germany.

[GitHub](https://github.com/Mohibullahmansoorvirk) · [LinkedIn](https://www.linkedin.com/in/mohibullah-mansoor-virk/)