# src/ingestion/producer.py
import json
import time
from kafka import KafkaProducer
from uuid import uuid4

producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def send(tx):
    producer.send('transactions', tx)
    producer.flush()

if __name__ == '__main__':
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument('--sample', default='data/sample_transactions.json')
    args = p.parse_args()
    with open(args.sample) as f:
        data = json.load(f)
    for tx in data:
        tx['transaction_id'] = str(uuid4())
        tx['timestamp'] = int(time.time()*1000)
        send(tx)
        time.sleep(0.01)