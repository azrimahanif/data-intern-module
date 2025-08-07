import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from data_transformers import transform_data

def test_transform_data_removes_invalid_rows():
    df = pd.DataFrame([
        {"customer_id": 1, "country": "USA", "amount": 100.0, "rating": 4.0, "age": 30, "email": "test@example.com"},
        {"customer_id": 2, "country": "Future Country", "amount": 100.0, "rating": 4.0, "age": 25, "email": "x@y.com"},
        {"customer_id": 3, "country": "UK", "amount": 150000.0, "rating": 4.0, "age": 50, "email": "a@b.com"},
        {"customer_id": 4, "country": "USA", "amount": 100.0, "rating": -1.0, "age": 40, "email": "user@email.com"},
        {"customer_id": 5, "country": "UK", "amount": 50.0, "rating": 4.0, "age": 130, "email": "abc@xyz.com"},
        {"customer_id": 6, "country": "USA", "amount": 100.0, "rating": 4.0, "age": 29, "email": "invalid-email.com"},
        {"customer_id": 7, "country": "UK", "amount": 100.0, "rating": 4.0, "age": 35, "email": "valid@email.com"},
    ])

    config = {
        "invalid_countries": ["Future Country", "Invalid Country"],
        "amount_threshold": 0,
        "rating_min": 0,
        "dropna": False,
    }

    cleaned_df = transform_data(df, config)

    # Expected only row 1 and 7 to remain (index 0 and 6)
    expected_ids = [1, 7]
    assert list(cleaned_df["customer_id"]) == expected_ids

