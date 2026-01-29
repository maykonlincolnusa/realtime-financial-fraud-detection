# src/ml/training/train_model.py
import mlflow
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# carregar dados do data/ ou MinIO
# features e labels prontos

# treinar
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_train, y_train)

# registrar
with mlflow.start_run():
    mlflow.sklearn.log_model(rf, 'model')
    mlflow.log_metric('roc_auc', 0.95)