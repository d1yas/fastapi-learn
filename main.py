from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing_extensions import List

app = FastAPI(
    title="Trading APP"
)

fake_users = [
    {"id": 1, "name": "John", "email": "bob"},
    {"id": 2, "name2": "John2", "email2": "bob2"},
    {"id": 3, "name3": "John3", "email3": "bob3"},
    {"id": 4, "name4": "Joh4", "email4": "bob4"},
]


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12 },
    {"id": 2, "user_id": 2, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12 },

]

@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


#----1---
class Trade(BaseModel):
    id: int
    user_id: int
    currency:str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float

@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}


#-----2-----