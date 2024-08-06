from pydantic import BaseModel, ConfigDict
from datetime import date, datetime
from typing import Optional


class TransAdd(BaseModel):
    owner: str
    amount: float
    date: Optional[str] = datetime.now().isoformat()
    category: str


class TransData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner: str
    amount: float
    date: date
    category: str
    
class Filtered(BaseModel):
    owner: str
    start_date: str
    end_date: str