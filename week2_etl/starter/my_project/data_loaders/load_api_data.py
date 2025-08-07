import logging
import requests
import pandas as pd
from dotenv import load_dotenv
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()

@data_loader
def load_data_from_api(*args, **kwargs):
    logger.info("🚀 Memulakan proses untuk load data dari API...")

    try:
        # Ganti dengan API sebenar anda
        api_url = "https://jsonplaceholder.typicode.com/posts"
        api_key = os.getenv("API_KEY")  # Optional, ikut API anda

        headers = {
            "Authorization": f"Bearer {api_key}"
        } if api_key else {}

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        df = pd.DataFrame(data)

        logger.info(f"Data processing completed successfully: {len(df)} baris.")
        return df

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
