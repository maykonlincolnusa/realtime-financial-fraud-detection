# src/processor/stream_processor.py
import json
from kafka import KafkaConsumer, KafkaProducer
import requests

consumer = KafkaConsumer('transactions', bootstrap_servers=['localhost:9092'], value_deserializer=lambda m: json.loads(m.decode('utf-8')))
producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

MODEL_SERVER = 'http://localhost:5000/score'

for msg in consumer:
    tx = msg.value
    # regra simples: transaction amount > 10000
    if tx.get('amount',0) > 10000:
        tx['rule_flag'] = 'high_amount'
    # chama scorer
    res = requests.post(MODEL_SERVER, json={'transaction': tx})
    score = res.json().get('score')
    tx['score'] = score
    if score > 0.8 or tx.get('rule_flag'):
        producer.send('alerts', tx)