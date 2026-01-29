# src/api/routes/alerts.py

from fastapi import APIRouter, Depends
from typing import List, Dict

# (opcional agora, mas já deixamos pronto)
# from src.api.security.auth import verify_token

router = APIRouter()

# Mock temporário (depois vem do Postgres)
FAKE_ALERTS_DB = [
    {
        "alert_id": "a1",
        "transaction_id": "tx123",
        "account_id": "acc001",
        "score": 0.93,
        "rule": "high_amount",
        "status": "OPEN"
    },
    {
        "alert_id": "a2",
        "transaction_id": "tx456",
        "account_id": "acc002",
        "score": 0.88,
        "rule": "velocity",
        "status": "REVIEW"
    }
]

@router.get("/", response_model=List[Dict])
def list_alerts():
    """
    Lista alertas de fraude.
    No futuro:
    - Busca no Postgres
    - Filtros por status, score, data
    - Paginação
    """
    return FAKE_ALERTS_DB


@router.get("/{alert_id}")
def get_alert(alert_id: str):
    """
    Retorna um alerta específico
    """
    for alert in FAKE_ALERTS_DB:
        if alert["alert_id"] == alert_id:
            return alert

    return {"error": "Alert not found"}