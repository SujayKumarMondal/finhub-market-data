from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import StockQuote
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message
router = APIRouter()

@router.get("/quote")
def get_stock_quote(symbol: str = Query(..., description="Stock symbol"), db: Session = Depends(get_db)):
    cache_key = f"stock_quote_{symbol}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("quote", {"symbol": symbol})
        stock = StockQuote(
            symbol=symbol,
            current_price=data.get("c"),
            high_price=data.get("h"),
            low_price=data.get("l"),
            open_price=data.get("o"),
            prev_close_price=data.get("pc")
        )
        db.add(stock)
        db.commit()
        cache_data(cache_key, data)
        
        publish_message("stock_quotes", {
        "symbol": stock.symbol,
        "current_price": stock.current_price,
        "high_price": stock.high_price,
        "low_price": stock.low_price,
        "open_price": stock.open_price,
        "prev_close_price": stock.prev_close_price
    })
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
