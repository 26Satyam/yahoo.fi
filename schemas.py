from pydantic import BaseModel

# Request model for fetching stock data
class StockDataRequest(BaseModel):
    symbol: str
    from_date: str
    to_date: str

# Response model for returning stock data
class StockDataResponse(BaseModel):
    open: float
    high: float
    low: float
    close: float
    timestamp: int
