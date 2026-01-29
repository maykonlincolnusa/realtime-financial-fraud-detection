# src/graph/neo4j_loader.py
from neo4j import GraphDatabase

uri = 'bolt://localhost:7687'
user = 'neo4j'
password = 'test'

class Neo4jLoader:
    def __init__(self):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    def close(self):
        self.driver.close()
    def create_tx(self, tx):
        with self.driver.session() as s:
            s.run(
                """
                MERGE (a:Account {id:$account_id})
                MERGE (m:Merchant {id:$merchant_id})
                MERGE (d:Device {id:$device_id})
                MERGE (i:IP {ip:$ip})
                MERGE (a)-[:USED_DEVICE]->(d)
                MERGE (d)-[:USED_IP]->(i)
                MERGE (a)-[:TRANSACTED_WITH {tx_id:$tx_id, amount:$amount, ts:$ts}]->(m)
                """,
                account_id=tx['account_id'], merchant_id=tx['merchant_id'], device_id=tx['device_id'], ip=tx['ip_address'], tx_id=tx['transaction_id'], amount=tx['amount'], ts=tx['timestamp']
            )