from pydantic import BaseModel
from typing import Optional


class WalletData(BaseModel):
    owner: str
    balance: Optional[float] = 0