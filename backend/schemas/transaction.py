from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class TransData(BaseModel):
    
    owner: str
    amount: float
    date: Optional[str] = datetime.now().strftime('%m/%d/%Y')
    category: str
