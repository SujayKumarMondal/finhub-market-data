# FastAPI Microservices Project – E-Commerce & Market Data Platform

🚀 Project Overview

This project is a full-stack FastAPI microservices platform that combines e-commerce functionalities with real-time market data analytics. It is designed for scalability, real-time updates, and modularity using microservices architecture, MySQL, and Redis Streams.

📂 Project Structure
fastapi-microservice/
│
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── models.py                   # SQLAlchemy models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── stock_service.py        # Stock quotes endpoints
│   │   ├── company_service.py      # Company profile endpoints
│   │   ├── news_service.py         # Market news endpoints
│   │   ├── forex_service.py        # Forex rates endpoints
│   │   └── crypto_service.py       # Crypto data endpoints
│   └── utils.py                    # Finnhub API helper, caching, formatting
│
├── db/
│   ├── __init__.py
│   ├── database.py                 # SQLAlchemy DB connection
│   └── crud.py                     # CRUD operations
│
├── services/
│   ├── auth_service.py             # User authentication endpoints
│   ├── order_service.py            # Orders creation & Redis publishing
│   ├── payment_service.py          # Payment processing consumer
│   └── product_service.py          # Product CRUD and syncing
│
├── utils/
│   ├── redis_producer.py           # Publish messages to Redis
│   ├── redis_consumer.py           # Consume messages from Redis
│   └── config.py                   # Environment variables & config
│
├── .env                            # DB, Redis, API keys
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation

🎯 Purpose & Use Cases

E-Commerce Module

CRUD operations for Products, Orders, Users.

Real-time order processing using Redis Streams.

Payment handling and status updates in background tasks.

Market Data Module

Fetch real-time stock quotes, crypto prices, forex rates, company profiles, and news from Finnhub API.

Cache data in Redis and persist in MySQL for historical analysis.

Publish market updates to Redis Streams for other microservices.

Collaboration & Extensibility

Modular microservices allow independent development and deployment.

Redis Streams enable real-time inter-service communication.

Fully documented API using Swagger.

⚙️ Workflows
1. E-Commerce Workflow

Product retrieval:

GET /products/ → fetch from MySQL or sync from external API.

Order creation:

POST /orders/ → order stored in MySQL.

Order data published to Redis stream.

Payment processing:

Redis consumer picks the order → marks as paid → updates DB.

Notification / Frontend update:

Other services or frontend can subscribe to Redis stream → receive real-time updates.

Flow Diagram:

[Frontend] → [FastAPI Order Service] → [MySQL] → [Redis Stream] → [Payment Service] → [MySQL update]

2. Market Data Workflow

API Request:

Example: GET /market/quote?symbol=AAPL.

Check Redis Cache:

If cached → return data immediately.

Else → fetch from Finnhub API.

Persist in MySQL:

Store structured data (StockQuote, CryptoData, ForexRate, MarketNews, CompanyProfile).

Publish to Redis:

Data is published to Redis streams → other services / dashboards can consume in real-time.

Flow Diagram:

[Frontend] → [Market API Service] → [Redis Cache check]
                   ↓
          [Finnhub API fetch]
                   ↓
              [MySQL storage]
                   ↓
             [Redis publish]
                   ↓
          [Subscribers / Dashboard]

🔗 Endpoints & Functionalities
Auth Service

GET /auth/ping – Health check.

Product Service

GET /products/ – Retrieve all products, optionally sync from public API.

Order Service

POST /orders/ – Create a new order and publish to Redis.

{
  "user_id": 1,
  "products": [1, 2],
  "total_amount": 100
}

Payment Service

GET /payments/start – Start Redis consumer to process and mark orders as paid.

Market Data Services
Endpoint	Method	Description
/market/quote	GET	Fetch real-time stock quotes
/market/company	GET	Fetch company profile information
/market/news	GET	Fetch market-related news for a symbol
/market/forex	GET	Fetch forex rates for a base currency
/market/crypto	GET	Fetch crypto data for a symbol

Redis Streams: All market data is published in real-time for other services to consume.

💻 Installation & Setup

Clone the repo:

git clone https://github.com/yourusername/fastapi-microservice.git
cd fastapi-microservice


Create virtual environment and install dependencies:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt


Configure .env file:

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=fastapi_microservice

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

PUBLIC_PRODUCT_API=https://fakestoreapi.com/products
FINNHUB_API_KEY=your_finnhub_api_key


Create MySQL tables or run migrations.

Run the FastAPI server:

uvicorn app.main:app --host 0.0.0.0 --port 8012 --reload


Access Swagger docs at http://127.0.0.1:8012/docs.

🔗 Useful Links

GitHub: https://github.com/yourusername/fastapi-microservice

LinkedIn: https://www.linkedin.com/in/sujay-mondal/

Finnhub API Docs: https://finnhub.io/docs/api

💡 Collaboration Guidelines

Use feature branches for development.

Follow PEP8.

Add docstrings and comments for all endpoints.

Push changes → create Pull Requests for review.

Redis and DB schema changes should be documented clearly.


| Key  | Meaning                                                          | Example      |
| ---- | ---------------------------------------------------------------- | ------------ |
| `c`  | **Current price** – The last traded price of the stock           | `245.5`      |
| `d`  | **Change** – Difference between current price and previous close | `7.62`       |
| `dp` | **Percent change** – Percentage change from previous close       | `3.2033`     |
| `h`  | **High price of the day** – Highest traded price today           | `246.3`      |
| `l`  | **Low price of the day** – Lowest traded price today             | `240.2106`   |
| `o`  | **Open price** – Price at market open                            | `241.225`    |
| `pc` | **Previous close** – Closing price of the previous trading day   | `237.88`     |
| `t`  | **Timestamp** – Unix timestamp of the quote                      | `1758312000` |
