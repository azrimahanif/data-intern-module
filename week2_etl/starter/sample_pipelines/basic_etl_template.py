# Basic ETL Pipeline Template for Mage.ai
# This template shows the structure for a complete ETL pipeline

import pandas as pd
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# DATA LOADER BLOCKS
# =============================================================================

def load_csv_data():
    """
    Data Loader: Extract data from CSV file
    """
    try:
        logger.info("Loading CSV data...")
        df = pd.read_csv('data_sources/sample_data.csv')
        logger.info(f"Loaded {len(df)} records from CSV")
        return df
    except Exception as e:
        logger.error(f"Error loading CSV data: {e}")
        raise

def load_api_data():
    """
    Data Loader: Extract data from API
    """
    try:
        import requests
        logger.info("Loading data from API...")
        
        # Example API call (replace with your API endpoint)
        api_url = "https://jsonplaceholder.typicode.com/users"
        response = requests.get(api_url)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data)
        logger.info(f"Loaded {len(df)} records from API")
        return df
    except Exception as e:
        logger.error(f"Error loading API data: {e}")
        raise

# =============================================================================
# TRANSFORMER BLOCKS
# =============================================================================

def clean_customer_data(df):
    """
    Transformer: Clean and validate customer data
    """
    try:
        logger.info("Cleaning customer data...")
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate records")
        
        # Handle missing values
        df['age'] = df['age'].fillna(df['age'].median())
        df['city'] = df['city'].fillna('Unknown')
        df['country'] = df['country'].fillna('Unknown')
        
        # Validate email format
        df = df[df['email'].str.contains('@', na=False)]
        
        # Convert date columns
        df['join_date'] = pd.to_datetime(df['join_date'], errors='coerce')
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'], errors='coerce')
        
        # Remove records with invalid dates
        df = df.dropna(subset=['join_date', 'last_purchase_date'])
        
        logger.info(f"Cleaned data: {len(df)} records remaining")
        return df
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        raise

def transform_customer_data(df):
    """
    Transformer: Create derived fields and aggregations
    """
    try:
        logger.info("Transforming customer data...")
        
        # Calculate customer lifetime (days since joining)
        df['customer_lifetime_days'] = (datetime.now() - df['join_date']).dt.days
        
        # Calculate days since last purchase
        df['days_since_last_purchase'] = (datetime.now() - df['last_purchase_date']).dt.days
        
        # Create customer segments based on spending
        df['customer_segment'] = df['monthly_spend'].apply(
            lambda x: 'High Value' if x >= 80 else 'Medium Value' if x >= 40 else 'Low Value'
        )
        
        # Create age groups
        df['age_group'] = df['age'].apply(
            lambda x: 'Young' if x < 30 else 'Adult' if x < 50 else 'Senior'
        )
        
        # Calculate total revenue potential
        df['revenue_potential'] = df['monthly_spend'] * 12
        
        logger.info("Data transformation completed")
        return df
    except Exception as e:
        logger.error(f"Error transforming data: {e}")
        raise

def aggregate_data(df):
    """
    Transformer: Create aggregated summaries
    """
    try:
        logger.info("Creating data aggregations...")
        
        # Customer count by segment
        segment_summary = df.groupby('customer_segment').agg({
            'customer_id': 'count',
            'monthly_spend': 'sum',
            'age': 'mean'
        }).rename(columns={'customer_id': 'customer_count'})
        
        # Customer count by country
        country_summary = df.groupby('country').agg({
            'customer_id': 'count',
            'monthly_spend': 'sum'
        }).rename(columns={'customer_id': 'customer_count'})
        
        # Subscription type distribution
        subscription_summary = df.groupby('subscription_type').agg({
            'customer_id': 'count',
            'monthly_spend': 'mean'
        }).rename(columns={'customer_id': 'customer_count'})
        
        logger.info("Data aggregation completed")
        return {
            'segment_summary': segment_summary,
            'country_summary': country_summary,
            'subscription_summary': subscription_summary
        }
    except Exception as e:
        logger.error(f"Error aggregating data: {e}")
        raise

# =============================================================================
# DATA EXPORTER BLOCKS
# =============================================================================

def save_cleaned_data(df):
    """
    Data Exporter: Save cleaned data to CSV
    """
    try:
        logger.info("Saving cleaned data...")
        output_path = 'submission/cleaned_customer_data.csv'
        df.to_csv(output_path, index=False)
        logger.info(f"Saved cleaned data to {output_path}")
        return df
    except Exception as e:
        logger.error(f"Error saving cleaned data: {e}")
        raise

def save_aggregated_data(aggregated_data):
    """
    Data Exporter: Save aggregated data to CSV files
    """
    try:
        logger.info("Saving aggregated data...")
        
        # Save each aggregation to separate files
        aggregated_data['segment_summary'].to_csv('submission/segment_summary.csv')
        aggregated_data['country_summary'].to_csv('submission/country_summary.csv')
        aggregated_data['subscription_summary'].to_csv('submission/subscription_summary.csv')
        
        logger.info("Saved all aggregated data files")
        return aggregated_data
    except Exception as e:
        logger.error(f"Error saving aggregated data: {e}")
        raise

def save_to_database(df):
    """
    Data Exporter: Save data to database (example with SQLite)
    """
    try:
        import sqlite3
        logger.info("Saving data to database...")
        
        # Create SQLite database connection
        conn = sqlite3.connect('submission/customer_data.db')
        
        # Save main data
        df.to_sql('customers', conn, if_exists='replace', index=False)
        
        # Create indexes for better performance
        conn.execute('CREATE INDEX IF NOT EXISTS idx_customer_id ON customers(customer_id)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_email ON customers(email)')
        conn.execute('CREATE INDEX IF NOT EXISTS idx_country ON customers(country)')
        
        conn.close()
        logger.info("Data saved to database successfully")
        return df
    except Exception as e:
        logger.error(f"Error saving to database: {e}")
        raise

# =============================================================================
# PIPELINE EXECUTION
# =============================================================================

def run_etl_pipeline():
    """
    Main ETL pipeline execution
    """
    try:
        logger.info("Starting ETL pipeline...")
        
        # Step 1: Extract data
        customer_data = load_csv_data()
        
        # Step 2: Transform data
        cleaned_data = clean_customer_data(customer_data)
        transformed_data = transform_customer_data(cleaned_data)
        aggregated_data = aggregate_data(transformed_data)
        
        # Step 3: Load data
        save_cleaned_data(transformed_data)
        save_aggregated_data(aggregated_data)
        save_to_database(transformed_data)
        
        logger.info("ETL pipeline completed successfully!")
        return {
            'cleaned_data': transformed_data,
            'aggregated_data': aggregated_data
        }
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_etl_pipeline() 