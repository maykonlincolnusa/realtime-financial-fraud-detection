# src/api/routes/graph.py
from fastapi import APIRouter
from src.api.services.graph_service import get_account_network

router = APIRouter()

@router.get("/account/{account_id}")
def account_graph(account_id: str):
    return get_account_network(account_id)