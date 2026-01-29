from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# Simulações temporárias (depois entram ML, regras, grafos e Kafka)
from src.rules.simple_rules import avaliar_regras
from src.models.ml_model import avaliar_modelo_ml
from src.graph.graph_engine import avaliar_grafo

router = APIRouter(prefix="/transactions", tags=["Transações"])


# =========================
# MODELO DA TRANSAÇÃO
# =========================
class Transaction(BaseModel):
    usuario_id: str
    conta_id: str
    valor: float
    moeda: str = "BRL"
    canal: str  # pix, cartao, transferencia
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# =========================
# ENDPOINT PRINCIPAL
# =========================
@router.post("/", summary="Receber transação e avaliar fraude")
def processar_transacao(transacao: Transaction):

    transaction_id = f"TX-{uuid.uuid4()}"
    timestamp = datetime.utcnow().isoformat()

    # =========================
    # 1. AVALIAÇÃO POR REGRAS
    # =========================
    score_regras, motivos_regras = avaliar_regras(transacao)

    # =========================
    # 2. AVALIAÇÃO POR ML
    # =========================
    score_ml = avaliar_modelo_ml(transacao)

    # =========================
    # 3. AVALIAÇÃO POR GRAFO
    # =========================
    score_grafo = avaliar_grafo(transacao)

    # =========================
    # 4. SCORE FINAL (ensemble)
    # =========================
    score_final = round(
        (score_regras * 0.4) +
        (score_ml * 0.4) +
        (score_grafo * 0.2),
        2
    )

    nivel_risco = (
        "ALTO" if score_final > 0.8
        else "MEDIO" if score_final > 0.5
        else "BAIXO"
    )

    alerta_gerado = score_final > 0.6

    # =========================
    # RESPOSTA
    # =========================
    return {
        "transaction_id": transaction_id,
        "timestamp": timestamp,
        "score_regras": score_regras,
        "score_ml": score_ml,
        "score_grafo": score_grafo,
        "score_final": score_final,
        "nivel_risco": nivel_risco,
        "alerta_gerado": alerta_gerado
    }