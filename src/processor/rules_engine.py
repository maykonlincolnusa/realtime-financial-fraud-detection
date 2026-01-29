# src/processor/rules_engine.py
import yaml
from typing import Dict

class RulesEngine:
    def __init__(self, path='rules/rules.yaml'):
        self.path = path
        self.reload()
    def reload(self):
        with open(self.path) as f:
            self.rules = yaml.safe_load(f)
    def evaluate(self, tx: Dict):
        flags = []
        for r in self.rules.get('rules', []):
            if r['type']=='threshold' and tx.get(r['field'],0) > r['value']:
                flags.append(r['id'])
        return flags