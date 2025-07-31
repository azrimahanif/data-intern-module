# Mage.ai Setup Guide

## 🚀 Quick Start with Mage.ai

### Prerequisites
- Docker Desktop installed and running
- Git installed
- Basic understanding of Python and SQL

### Step 1: Install Mage.ai

```bash
# Clone the Mage.ai repository
git clone https://github.com/mage-ai/mage-ai.git
cd mage-ai

# Start Mage.ai using Docker Compose
docker-compose up -d
```

### Step 2: Access Mage.ai

1. Open your web browser
2. Navigate to: `http://localhost:6789`
3. You should see the Mage.ai welcome screen

### Step 3: Create Your First Project

1. Click "Create new project"
2. Enter project name: `AI_Knowledge_Assistant_ETL`
3. Choose "Python" as the project type
4. Click "Create project"

### Step 4: Understanding the Interface

#### Main Components:
- **Pipelines**: Your ETL workflows
- **Blocks**: Individual processing units
- **Triggers**: Automated execution rules
- **Settings**: Project configuration

#### Block Types:
- **Data Loaders**: Extract data from sources
- **Transformers**: Process and transform data
- **Data Exporters**: Load data to destinations

### Step 5: Create Your First Pipeline

1. Click "New pipeline"
2. Name it: `week2_basic_etl`
3. Click "Create pipeline"

#### Add a Data Loader:
1. Click "Add block" → "Data loader"
2. Choose "Python" as the block type
3. Name it: `load_csv_data`
4. Add this code:

```python
import pandas as pd

def load_data():
    # Load sample CSV data
    df = pd.read_csv('data_sources/sample_data.csv')
    return df
```

#### Add a Transformer:
1. Click "Add block" → "Transformer"
2. Choose "Python" as the block type
3. Name it: `clean_data`
4. Add this code:

```python
def transform_data(df):
    # Basic data cleaning
    df = df.dropna()
    df = df.drop_duplicates()
    return df
```

#### Add a Data Exporter:
1. Click "Add block" → "Data exporter"
2. Choose "Python" as the block type
3. Name it: `save_cleaned_data`
4. Add this code:

```python
def export_data(df):
    # Save cleaned data
    df.to_csv('submission/cleaned_data.csv', index=False)
    return df
```

### Step 6: Connect Blocks

1. Click on the output of `load_csv_data`
2. Drag to connect it to `clean_data` input
3. Click on the output of `clean_data`
4. Drag to connect it to `save_cleaned_data` input

### Step 7: Test Your Pipeline

1. Click "Run pipeline" button
2. Watch the execution in real-time
3. Check the logs for any errors
4. Verify the output file is created

## 🛠️ Advanced Setup

### Environment Variables
Create a `.env` file in your project root:

```env
# Database connections
DB_HOST=localhost
DB_PORT=5432
DB_NAME=etl_database
DB_USER=your_username
DB_PASSWORD=your_password

# API keys
API_KEY=your_api_key
API_SECRET=your_api_secret
```

### Custom Blocks
You can create reusable blocks for common operations:

```python
# Example: API Data Loader
import requests
import pandas as pd

def load_api_data(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return pd.DataFrame(data)
```

## 📊 Monitoring and Logging

### Pipeline Monitoring
- View pipeline execution history
- Monitor block performance
- Set up alerts for failures

### Logging Best Practices
```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def your_function():
    logger.info("Starting data processing")
    try:
        # Your code here
        logger.info("Data processing completed successfully")
    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise
```

## 🔧 Troubleshooting

### Common Issues:

1. **Docker not running**
   - Start Docker Desktop
   - Wait for it to fully load

2. **Port 6789 already in use**
   - Change port in docker-compose.yml
   - Or stop other services using that port

3. **Permission errors**
   - Run Docker commands with sudo (Linux/Mac)
   - Check Docker Desktop settings (Windows)

4. **Pipeline fails to run**
   - Check block connections
   - Verify input data exists
   - Review error logs

### Getting Help:
- [Mage.ai Documentation](https://docs.mage.ai/)
- [Mage.ai GitHub Issues](https://github.com/mage-ai/mage-ai/issues)
- [Mage.ai Community](https://www.mage.ai/community)

## 🎯 Next Steps

1. Complete the basic pipeline setup
2. Experiment with different data sources
3. Try SQL transformers
4. Set up scheduling and triggers
5. Build your Week 2 assignments

---

**Remember**: Mage.ai is designed to be intuitive. Don't hesitate to experiment and explore the interface! 