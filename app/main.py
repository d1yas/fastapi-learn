from fastapi import FastAPI
from .routers import users, attachments, tickets, comments


app = FastAPI()
app.include_router(users.router)
app.include_router(tickets.router)
# app.include_router(users.router)
# app.include_router(users.router)
