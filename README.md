Absolutely! Here’s a **full, cleaned-up README.md** for your FastAPI microservices project, with:

* Properly formatted folder structure
* Tech stack
* Workflows
* Installation instructions
* Market data endpoints as per your request
* Social links and collaboration guidelines

```markdown
# FastAPI Microservices Project – E-Commerce & Market Data Platform

🚀 **Project Overview**  

This project is a full-stack FastAPI microservices platform that combines e-commerce functionalities with real-time market data analytics. It is designed for scalability, real-time updates, and modularity using microservices architecture, MySQL, and Redis Streams.

---

## 📂 Project Structure

```

fastapi-microservice/
│
├── app/
│   ├── **init**.py
│   ├── main.py                     # FastAPI app entry point
│   ├── models.py                   # SQLAlchemy models
│   ├── services/
│   │   ├── **init**.py
│   │   ├── stock\_service.py        # Stock quotes endpoints
│   │   ├── company\_service.py      # Company profile endpoints
│   │   ├── news\_service.py         # Market news endpoints
│   │   ├── forex\_service.py        # Forex rates endpoints
│   │   └── crypto\_service.py       # Crypto data endpoints
│   └── utils.py                    # Finnhub API helper, caching, formatting
│
├── db/
│   ├── **init**.py
│   ├── database.py                 # SQLAlchemy DB connection
│   └── crud.py                     # CRUD operations
│
├── services/
│   ├── auth\_service.py             # User authentication endpoints
│   ├── order\_service.py            # Orders creation & Redis publishing
│   ├── payment\_service.py          # Payment processing consumer
│   └── product\_service.py          # Product CRUD and syncing
│
├── utils/
│   ├── redis\_producer.py           # Publish messages to Redis
│   ├── redis\_consumer.py           # Consume messages from Redis
│   └── config.py                   # Environment variables & config
│
├── .env                            # DB, Redis, API keys
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation

```

---

## 🎯 Purpose & Use Cases

### E-Commerce Module
- CRUD operations for Products, Orders, Users.  
- Real-time order processing using Redis Streams.  
- Payment handling and status updates in background tasks.  

### Market Data Module
- Fetch real-time stock quotes, crypto prices, forex rates, company profiles, and news from Finnhub API.  
- Cache data in Redis and persist in MySQL for historical analysis.  
- Publish market updates to Redis Streams for other services.  

### Collaboration & Extensibility
- Modular microservices allow independent development and deployment.  
- Redis Streams enable real-time inter-service communication.  
- Fully documented API using Swagger.  

---

## ⚙️ Workflows

### 1. E-Commerce Workflow
1. **Product retrieval:** `GET /products/` → fetch from MySQL or sync from external API.  
2. **Order creation:** `POST /orders/` → store order in MySQL and publish to Redis stream.  
3. **Payment processing:** Redis consumer picks the order → marks as paid → updates DB.  
4. **Notification / Frontend update:** Other services or frontend can subscribe to Redis stream → receive real-time updates.  

**Flow Diagram:**  
```

\[Frontend] → \[FastAPI Order Service] → \[MySQL] → \[Redis Stream] → \[Payment Service] → \[MySQL update]

```

### 2. Market Data Workflow
1. **API Request:** Example: `GET /market/quote?symbol=AAPL`.  
2. **Check Redis Cache:** If cached → return data immediately, else fetch from Finnhub API.  
3. **Persist in MySQL:** Store structured data (StockQuote, CryptoData, ForexRate, MarketNews, CompanyProfile).  
4. **Publish to Redis:** Data is published to Redis streams → other services / dashboards can consume in real-time.  

**Flow Diagram:**  
```

\[Frontend] → \[Market API Service] → \[Redis Cache check]
↓
\[Finnhub API fetch]
↓
\[MySQL storage]
↓
\[Redis publish]
↓
\[Subscribers / Dashboard]

````

---

## 🔗 Endpoints & Functionalities

### Auth Service
- `GET /auth/ping` – Health check.

### Product Service
- `GET /products/` – Retrieve all products, optionally sync from public API.

### Order Service
- `POST /orders/` – Create a new order and publish to Redis.  
Example body:
```json
{
  "user_id": 1,
  "products": [1, 2],
  "total_amount": 100
}
````

### Payment Service

* `GET /payments/start` – Start Redis consumer to process and mark orders as paid.

### Market Data Services

| Category      | Method & Endpoint       | Description           | Response                                                           |
| ------------- | ----------------------- | --------------------- | ------------------------------------------------------------------ |
| Stock Market  | GET /market/quote       | Get Stock Quote       | Returns current price, open, high, low, previous close of a stock. |
| Company       | GET /market/company     | Get Company Profile   | Returns company name, logo, market cap, sector, and exchange info. |
| News          | GET /market/news        | Get Market News       | Returns latest market news headlines and sources.                  |
| Calendar      | GET /calendar/earnings  | Get Earnings Calendar | Returns upcoming earnings reports with dates and companies.        |
| Calendar      | GET /calendar/ipos      | Get IPO Calendar      | Returns upcoming IPOs with date, symbol, and exchange.             |
| Economic Data | GET /economic/countries | Get Countries         | Returns country info including currency, timezone, and risk data.  |

> Redis Streams: All market data is published in real-time for other services to consume.

---

## 💻 Installation & Setup

1. Clone the repo:

```bash
git clone https://github.com/SujayKumarMondal/finhub-market-data.git
cd fastapi-microservice
```

2. Create virtual environment and install dependencies:

```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure `.env` file:

```
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=yourpassword
MYSQL_DB=fastapi_microservice

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

FINNHUB_API_KEY=your_finnhub_api_key
```

4. Create MySQL tables or run migrations.

5. Run the FastAPI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8012 --reload
```

6. Access Swagger docs: [http://127.0.0.1:8012/docs](http://127.0.0.1:8012/docs)

---

## 🔗 Useful Links

* GitHub: [https://github.com/SujayKumarMondal/finhub-market-data](https://github.com/SujayKumarMondal/finhub-market-data)
* LinkedIn: [https://www.linkedin.com/in/sujay-mondal/](https://www.linkedin.com/in/sujay-mondal/)
* Finnhub API Docs: [https://finnhub.io/docs/api](https://finnhub.io/docs/api)

---

## 💡 Collaboration Guidelines

* Use feature branches for development.
* Follow PEP8.
* Add docstrings and comments for all endpoints.
* Push changes → create Pull Requests for review.
* Redis and DB schema changes should be documented clearly.

---

## 📊 Stock Quote Keys

| Key  | Meaning                                                | Example    |
| ---- | ------------------------------------------------------ | ---------- |
| `c`  | Current price – The last traded price of the stock     | 245.5      |
| `d`  | Change – Difference from previous close                | 7.62       |
| `dp` | Percent change – Percentage change from previous close | 3.2033     |
| `h`  | High price of the day                                  | 246.3      |
| `l`  | Low price of the day                                   | 240.2106   |
| `o`  | Open price                                             | 241.225    |
| `pc` | Previous close                                         | 237.88     |
| `t`  | Timestamp – Unix timestamp of the quote                | 1758312000 |
