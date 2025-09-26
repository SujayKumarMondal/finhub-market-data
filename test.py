# import os

# # Root directory
# root_dir = r"D:\SUJAY\Projects\fastapi-microservice"

# # Define folders and files structure
# structure = {
#     "": ["fastapi_server.py", ".env", "README.md"],
#     "services": ["product_service.py", "order_service.py", "payment_service.py", "auth_service.py"],
#     "db": ["models.py", "crud.py", "database.py"],
#     "utils": ["kafka_producer.py", "kafka_consumer.py", "config.py"]
# }

# # Function to create folders and files
# for folder, files in structure.items():
#     folder_path = os.path.join(root_dir, folder)
#     os.makedirs(folder_path, exist_ok=True)
#     for file in files:
#         file_path = os.path.join(folder_path, file)
#         if not os.path.exists(file_path):
#             with open(file_path, "w") as f:
#                 f.write("")  # create empty file
#             print(f"Created file: {file_path}")
#         else:
#             print(f"File already exists: {file_path}")

# print("\nProject structure created successfully!")




import finnhub
from dotenv import load_dotenv
load_dotenv()
import os
# Replace with your API key
api_key = os.environ.get("FINNHUB_API_KEY")
finnhub_client = finnhub.Client(api_key=api_key)

tests = {
    "Quote": lambda: finnhub_client.quote("AAPL"),
    "Company Profile": lambda: finnhub_client.company_profile2(symbol="AAPL"),
    "News": lambda: finnhub_client.general_news("general", min_id=0),
    "Earnings Calendar": lambda: finnhub_client.earnings_calendar(_from="2025-09-01", to="2025-09-30"),
    "IPO Calendar": lambda: finnhub_client.ipo_calendar(_from="2025-09-01", to="2025-12-31"),
    "Countries": lambda: finnhub_client.country(),
    "Candles": lambda: finnhub_client.stock_candles("AAPL", "D", 1609459200, 1612137600),
    "Dividends": lambda: finnhub_client.stock_dividends("AAPL", _from="2024-01-01", to="2025-01-01"),
    "Financials": lambda: finnhub_client.financials("AAPL", "annual", ""),
    "Metrics": lambda: finnhub_client.company_basic_financials("AAPL", "all"),
    "Recommendations": lambda: finnhub_client.recommendation_trends("AAPL"),
    "Insider Transactions": lambda: finnhub_client.stock_insider_transactions("AAPL", _from="2024-01-01", to="2025-01-01"),
    "Ownership": lambda: finnhub_client.ownership("AAPL"),
    "Symbol Search": lambda: finnhub_client.symbol_lookup("Tesla"),
    "Forex Rates": lambda: finnhub_client.forex_rates(base="USD"),
    "Crypto Candles": lambda: finnhub_client.crypto_candles("BINANCE:BTCUSDT", "D", 1609459200, 1612137600),
}

for name, func in tests.items():
    try:
        result = func()
        print(f"✅ {name} works (sample keys: {list(result.keys())[:5] if isinstance(result, dict) else type(result)})")
    except Exception as e:
        print(f"❌ {name} not available: {e}")
