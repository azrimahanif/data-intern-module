"""
config.py
----------
Configuration constants for vector DB project.
"""

from pathlib import Path

# tempat simpan database local (guna ChromaDB sebagai contoh)
VECTOR_DB_DIR = Path("./data/vector_db")

# tempat log analytics
ANALYTICS_DIR = Path("./data/analytics")
SEARCH_LOG_CSV = ANALYTICS_DIR / "search_logs.csv"
