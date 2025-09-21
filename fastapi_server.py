from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services import stock_service, company_service, news_service, calendar_service, economic_service

app = FastAPI(title="Financial Microservice Project")

# Home page route
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def home(request: Request, ):
    return templates.TemplateResponse("index.html", {"request": request})

# Include routers
app.include_router(stock_service.router, prefix="/market", tags=["Stock Market"])
app.include_router(company_service.router, prefix="/market", tags=["Company"])
app.include_router(news_service.router, prefix="/market", tags=["News"])
app.include_router(calendar_service.router, prefix="/calendar", tags=["Calendar"])
app.include_router(economic_service.router, prefix="/economic", tags=["Economic Data"])

# Setup templates
templates = Jinja2Templates(directory="app/templates")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_server:app", host="127.0.0.1", port=8012, reload=True)
