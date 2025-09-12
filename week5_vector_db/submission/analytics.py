# submission/analytics.py
import time
import json
from threading import Lock
from collections import Counter

class Analytics:
    """Simple file-backed analytics + in-memory counters."""
    def __init__(self, path: str = "./data/search_analytics.jsonl"):
        self.path = path
        self.lock = Lock()
        self.counter = Counter()
        self.total_latency = 0.0
        self.total_queries = 0

    def record_query(self, query: str, n_results: int, latency: float):
        entry = {
            "ts": time.time(),
            "query": query,
            "n_results": n_results,
            "latency": latency
        }
        with self.lock:
            # append a JSON line
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            self.counter[query] += 1
            self.total_latency += latency
            self.total_queries += 1

    def stats(self):
        with self.lock:
            avg_latency = (self.total_latency / self.total_queries) if self.total_queries else 0.0
            top_queries = self.counter.most_common(10)
            return {
                "total_queries": self.total_queries,
                "avg_latency": avg_latency,
                "top_queries": top_queries
            }
