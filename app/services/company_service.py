from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.database import get_db
from app.models import CompanyProfile
from app.utils import fetch_finnhub_data, cache_data, get_cached_data
from utils.redis_producer import publish_message

router = APIRouter()

@router.get("/company")
def get_company_profile(symbol: str = Query(..., description="Company symbol"), db: Session = Depends(get_db)):
    cache_key = f"company_profile_{symbol}"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    try:
        data = fetch_finnhub_data("stock/profile2", {"symbol": symbol})
        company = CompanyProfile(
            symbol=symbol,
            name=data.get("name"),
            exchange=data.get("exchange"),
            industry=data.get("finnhubIndustry"),
            logo=data.get("logo"),
            data=data
        )
        db.add(company)
        db.commit()
        cache_data(cache_key, data)
        
        publish_message("company_profiles", {
            "id": company.id,
            "symbol": company.symbol,
            "name": company.name,
            "exchange": company.exchange,
            "industry": company.industry,
            "logo": company.logo,
            "data": company.data
        })
                
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
