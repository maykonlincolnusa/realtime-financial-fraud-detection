# src/api/routes/alerts.py
from fastapi import APIRouter
from src.api.services.alert_service import list_alerts

router = APIRouter()

@router.get("/")
def get_alerts(limit: int = 100):
    return list_alerts(limit)