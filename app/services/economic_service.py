from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import Country
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message
from datetime import datetime

router = APIRouter()

# ---------------- COUNTRIES ----------------
@router.get("/countries")
def get_countries(db: Session = Depends(get_db)):
    cache_key = "countries"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("country", {})
        for item in data:
            
            code = item.get("code2") or "N/A"
            name = item.get("country") or "Unknown"
            currency = item.get("currency") or "Unknown"
            timezone = item.get("timezone")
            
            country = Country(
                # code=item.get("code2"),      # maps to 'code' column
                # name=item.get("country"), 
                # currency=item.get("currency"),
                # timezone=item.get("timezone"),
                # data=item
                
                code=code,                  # no trimming
                name=name[:100],             # keep name length safe
                currency=currency[:100],     # long currency names allowed
                timezone=timezone[:50] if timezone else None,
                data=item
            )
            db.add(country)
        db.commit()

        cache_data(cache_key, data)

        publish_message("countries", {"count": len(data)})

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


