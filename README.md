realtime-financial-fraud-detection

> Sistema de Detecção de Fraude Financeira em Tempo Real



Resumo: este repositório contém uma arquitetura end-to-end para ingestão de transações em tempo real, processamento (streaming), análise de grafos, scoring por modelos de machine learning, acionamento de regras e interfaces para observabilidade e deploy em produção.


---

Índice

1. Visão Geral


2. Principais Recursos


3. Arquitetura


4. Tecnologias Principais


5. Estrutura do Repositório


6. Pré-requisitos


7. Execução Rápida (local)


8. Simular Dados de Transação


9. Tópicos Kafka e Payloads de Exemplo


10. Pipeline de ML — Treino e Deploy


11. Análise de Grafos (Neo4j)


12. Observabilidade e Métricas


13. Deploy (Kubernetes / Terraform)


14. Segurança e Compliance


15. Testes e CI/CD


16. Roadmap / Próximos passos


17. Contribuição


18. Licença


19. Contato




---

Visão Geral

Este projeto demonstra uma solução prática e replicável para detectar fraudes financeiras em tempo real. A abordagem combina:

Ingestão de eventos com Kafka;

Processamento em streaming (ex.: Flink / Kafka Streams / Spark Structured Streaming);

Motor de regras para decisões rápidas (low-latency);

Modelos de ML para scoring (batch e online);

Análise relacional em grafos (Neo4j) para identificar redes de contas e anomalias;

Observabilidade (logs, traces, métricas) e infra como código para deploy.


O objetivo é permitir que desenvolvedores e engenheiros de dados repliquem um ambiente para testes e POC, com caminhos claros para produção.


---

Principais Recursos

Arquitetura modular (ingestão, processamento, feature store, model serving, grafos, UI).

Exemplo de docker-compose para levantar ambiente local com Kafka, Zookeeper, Neo4j e serviços mínimos.

Scripts para simular transações e validar o fluxo end-to-end.

Estrutura para treinos de modelos e deploy (MLflow/BentoML/Seldon como exemplos).

Regras configuráveis + fallback para intervenção humana.



---

Arquitetura

[Producers] --> Kafka Topics --> [Stream Processor (Flink/Kafka Streams)] -->
  --> Feature Store (Feast / ClickHouse) --> Model Scoring Service --> Decisions --> Actions
                                      |                                 |
                                      v                                 v
                                   Neo4j (graph)                   Alerting / Dashboard

Notas:

O processor aplica enrichments, features em tempo real e consulta o feature store para scoring.

Neo4j é usado para detectar relações (ex.: shared devices, same recipient patterns).



---

Tecnologias Principais

Kafka, Zookeeper

Apache Flink / Kafka Streams (exemplos de processamento)

Neo4j

Feast (feature store) ou alternativa (ClickHouse, Redis)

MLflow / BentoML / Seldon (model registry e serving)

Docker / docker-compose para desenvolvimento local

Kubernetes + Helm + Terraform para produção

Grafana / Prometheus / ELK para observabilidade



---

Estrutura do Repositório

Sugestão de estrutura (adapte conforme o repo atual):

/infra                # Terraform, k8s manifests, helm charts
/docker               # Dockerfiles e compose
/services
  /ingestor           # Producer e simulador de transações
  /processor          # Flink / stream processing jobs
  /scorer             # Serviço HTTP de scoring (model serving)
  /rules-engine       # Motor de regras
  /graph-service      # Scripts e integração com Neo4j
/ml
  /training           # Notebooks e pipelines de treino
  /models             # Model artifacts, MLflow
/scripts              # utilitários: create topics, seed data
/docs                 # diagramas, especificações, payloads
/tests                # testes unitários e integração
README.md


---

Pré-requisitos

Docker e docker-compose

Java (se usar Flink)

Python 3.9+

Kafka client (opcional)

Neo4j Desktop / container



---

Execução Rápida (local)

Exemplo mínimo com docker-compose (supõe docker-compose.yml já presente):

# Subir infra mínima
docker compose up -d zookeeper kafka neo4j
# Opcional: levantar serviços básicos
docker compose up -d ingestor processor scorer

# Ver logs
docker compose logs -f processor

Comandos úteis

# criar tópicos kafka (exemplo)
./scripts/create_kafka_topics.sh

# rodar simulador de transações
python services/ingestor/send_fake_transactions.py --rate 20


---

Simular Dados de Transação

Inclua um script send_fake_transactions.py que publique mensagens no tópico transactions. Exemplo de payload (JSON):

{
  "transaction_id": "tx_0001",
  "timestamp": "2025-01-29T12:00:00Z",
  "amount": 1250.50,
  "currency": "BRL",
  "card_id": "card_1234",
  "merchant_id": "m_987",
  "merchant_category": "retail",
  "customer_id": "cust_555",
  "merchant_country": "BR",
  "card_present": false,
  "device_id": "dev_111",
  "ip_address": "200.160.0.1",
  "status": "pending"
}


---

Tópicos Kafka e Payloads de Exemplo

Tópicos sugeridos:

transactions — eventos brutos de transação

enriched-transactions — transações com enrichments e features

scores — resultado do scoring (json com score e decisão)

alerts — eventos que devem gerar alerta/manual review


Exemplo de mensagem em scores

{
  "transaction_id": "tx_0001",
  "score": 0.87,
  "model_version": "v1.2.0",
  "decision": "block",
  "reason": "high_risk_graph_pattern"
}


---

Pipeline de ML — Treino e Deploy

1. Dados históricos → features offline → treino de modelos (XGBoost, LightGBM, NN)


2. Registrar modelo no MLflow (versioning)


3. Pack & serve (BentoML / Seldon)


4. Stream processor envia features ao serviço de scoring por gRPC/HTTP


5. Feedback loop: rotular casos revisados para re-treino periódico



Métricas importantes

Precision, Recall, F1 (especialmente Recall em fraudes)

ROC AUC

Taxa de falsos positivos (FP rate)

Latência de scoring (p95, p99)


Comando exemplo para treino (placeholder)

python ml/training/train_model.py --config ml/configs/experiment.yaml
mlflow ui  # visualizar runs


---

Análise de Grafos (Neo4j)

Modelar entidades (card, customer, device, merchant) como nós e relações (used_by, transacted_at) como arestas.

Scripts em services/graph-service para popular o banco a partir de enriched-transactions.

Consultas típicas:

detectar clusters de dispositivos compartilhados

caminhos de transações entre contas



Exemplo de cypher

MATCH (c:Card)-[:USED_ON]->(d:Device)
WITH d, collect(distinct c.card_id) AS cards
WHERE size(cards) > 3
RETURN d.device_id, cards


---

Observabilidade e Métricas

Prometheus para métricas, Grafana para dashboards.

Logs centralizados (ELK / Loki).

Tracing distribuído (Jaeger / OpenTelemetry).


Dashboards sugeridos

Volume de transações por minuto

Latência do pipeline

Distribuição de scores

Alertas / taxa de aprovação manual



---

Deploy (Kubernetes / Terraform)

Criar helm charts para cada serviço (processor, scorer, ingestor, graph-ingest).

Terraform para infra cloud (EKS/GKE/AKS, VPC, Managed Kafka se disponível).

Use k8s Horizontal Pod Autoscaler (HPA) para scorer e processor.


Pontos críticos

Isolar segredos (HashiCorp Vault / Kubernetes secrets)

TLS entre serviços e Kafka

Backup e retenção de dados do Neo4j e feature store



---

Segurança e Compliance

Encriptar dados sensíveis em repouso e em trânsito.

Anonimizar/mascarar dados PII em ambientes de dev.

Política de acesso baseada em papéis (RBAC) para dashboards e banco de dados.

Conformidade LGPD / GDPR: armazenar consentimentos e rastro de processamento.



---

Testes e CI/CD

Unit tests para componentes (pytest).

Testes de integração com testcontainers (levantar Kafka/Neo4j temporários).

Pipeline de CI que:

roda lint e testes

builda imagens Docker

publica artefatos (registry) e atualiza ambiente de staging


---

Contribuição

1. Fork o repositório


2. Crie uma branch feature/xxx


3. Abra PR com descrição clara e testes



Por favor escreva issues detalhadas e marque help wanted para tarefas que você espera colaboração.


---

Licença

MIT


---

Contato

maykon_zero@hotmail.com 
maykonlincoln.com 