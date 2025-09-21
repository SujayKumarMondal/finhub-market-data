from sqlalchemy import Column, Integer, String, Float, JSON
from db.database import Base

class StockQuote(Base):
    __tablename__ = "stock_quotes"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    current_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    open_price = Column(Float)
    prev_close_price = Column(Float)

class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    name = Column(String(255))
    exchange = Column(String(50))
    industry = Column(String(100))
    logo = Column(String(255))
    data = Column(JSON)


from sqlalchemy import Column, Integer, String, Float, Date, JSON
from db.database import Base


# ---------------- MARKET NEWS ----------------
class MarketNews(Base):
    __tablename__ = "market_news"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20))
    headline = Column(String(255))
    source = Column(String(255))
    url = Column(String(255))
    datetime = Column(Integer)
    

# ---------------- EARNINGS CALENDAR ----------------
class EarningsCalendar(Base):
    __tablename__ = "earnings_calendar"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    date = Column(Date)
    eps_estimate = Column(Float)
    eps_actual = Column(Float)
    revenue_estimate = Column(Float)
    revenue_actual = Column(Float)
    data = Column(JSON)  # store raw response for flexibility


# ---------------- IPO CALENDAR ----------------
class IPOCalendar(Base):
    __tablename__ = "ipo_calendar"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20))
    company = Column(String(255))
    date = Column(Date)
    exchange = Column(String(50))
    price_range = Column(String(50))
    shares = Column(Integer)
    expected_amount = Column(Float)
    data = Column(JSON)


# ---------------- ECONOMIC EVENTS ----------------
class EconomicEvent(Base):
    __tablename__ = "economic_events"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(100))
    event = Column(String(255))
    impact = Column(String(50))
    actual = Column(String(50))
    forecast = Column(String(50))
    previous = Column(String(50))
    date = Column(Date)
    data = Column(JSON)
    
    
# ---------------- COUNTRIES ----------------
class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False)   # e.g., "US"
    name = Column(String(100), nullable=False)  # e.g., "United States"
    currency = Column(String(100))               # e.g., "USD"
    timezone = Column(String(50)) 
    data = Column(JSON)  # store full raw API response


