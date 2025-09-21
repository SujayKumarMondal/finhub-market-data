from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import EarningsCalendar, IPOCalendar
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message
from datetime import datetime

router = APIRouter()

# ---------------- EARNINGS CALENDAR ----------------
@router.get("/earnings")
def get_earnings_calendar(
    _from: str = Query("2025-01-01", description="Start date"),
    to: str = Query("2025-12-31", description="End date"),
    db: Session = Depends(get_db)
):
    cache_key = f"earnings_calendar_{_from}_{to}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("calendar/earnings", {"from": _from, "to": to})
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


# ---------------- IPO CALENDAR ----------------
@router.get("/ipos")
def get_ipo_calendar(
    _from: str = Query("2025-01-01", description="Start date"),
    to: str = Query("2025-12-31", description="End date"),
    db: Session = Depends(get_db)
):
    cache_key = f"ipo_calendar_{_from}_{to}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("calendar/ipo", {"from": _from, "to": to})
        items = data.get("ipoCalendar", [])

        for item in items:
            ipo = IPOCalendar(
                symbol=item.get("symbol"),
                company=item.get("name"),
                date=datetime.strptime(item.get("date"), "%Y-%m-%d").date() if item.get("date") else None,
                exchange=item.get("exchange"),
                price_range=item.get("price"),
                shares=item.get("numberOfShares"),
                expected_amount=item.get("totalSharesValue"),
                data=item
            )
            db.add(ipo)
        db.commit()

        cache_data(cache_key, items)

        # publish summary to Redis
        publish_message("ipo_calendar", {
            "from": _from,
            "to": to,
            "count": len(items)
        })

        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
