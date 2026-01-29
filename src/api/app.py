# src/api/app.py

from fastapi import FastAPI
from src.api.routes import (
    alerts,
    transactions,
    graph
)

app = FastAPI(title="Fraud Detection API")

app.include_router(
    alerts.router,
    prefix="/alerts",
    tags=["Alerts"]
)

app.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transactions"]
)

app.include_router(
    graph.router,
    prefix="/graph",
    tags=["Graph"]
)