from sqlalchemy.orm import Session
from app.models import StockQuote, CompanyProfile, MarketNews, ForexRate, CryptoData

def create_stock_quote(db: Session, quote: StockQuote):
    db.add(quote)
    db.commit()
    db.refresh(quote)
    return quote

def create_company_profile(db: Session, profile: CompanyProfile):
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

def create_market_news(db: Session, news: MarketNews):
    db.add(news)
    db.commit()
    db.refresh(news)
    return news


