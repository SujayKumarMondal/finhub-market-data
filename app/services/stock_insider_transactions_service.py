from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import EarningsCalendar, IPOCalendar
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message
from datetime import datetime

router = APIRouter()



@router.get("/stock/insider-transactions")
def get_stock_insider_transactions(
    symbol: str = Query("Symbol"),
    _from: str = Query("2025-01-01", description="Start date"),
    to: str = Query("2025-12-31", description="End date"),
    db: Session = Depends(get_db)
):
    cache_key = f"stock_insider_transactions{_from}_{to} for Symbol: {symbol}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("/stock/insider-transactions", {"symbol": symbol, "from": _from, "to": to})
        items = data.get("earningsCalendar", [])

        for item in items:
            earnings = EarningsCalendar(
                symbol=item.get("symbol"),
                date=datetime.strptime(item.get("date"), "%Y-%m-%d").date() if item.get("date") else None,
                eps_estimate=item.get("epsEstimate"),
                eps_actual=item.get("epsActual"),
                revenue_estimate=item.get("revenueEstimate"),
                revenue_actual=item.get("revenueActual"),
                data=item
            )
            db.add(earnings)
        db.commit()

        cache_data(cache_key, items)

        # publish summary to Redis
        publish_message("earnings_calendar", {
            "from": _from,
            "to": to,
            "count": len(items)
        })

        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))