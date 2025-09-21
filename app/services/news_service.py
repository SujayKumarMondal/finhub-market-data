from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import MarketNews
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message

router = APIRouter()

@router.get("/news")
def get_market_news(symbol: str = Query(...), db: Session = Depends(get_db)):
    cache_key = f"market_news_{symbol}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("company-news", {"symbol": symbol, "from": "2025-01-01", "to": "2025-12-31"})
        for item in data:
            news = MarketNews(
                symbol=symbol,
                headline=item.get("headline"),
                source=item.get("source"),
                url=item.get("url"),
                datetime=item.get("datetime")
            )
            db.add(news)
        db.commit()
        cache_data(cache_key, data)
        
        publish_message("market_news", {
                "id": news.id,
                "symbol": news.symbol,
                "headline": news.headline,
                "source": news.source,
                "url": news.url,
                "datetime": news.datetime
            })
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
