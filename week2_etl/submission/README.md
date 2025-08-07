# Week 2 Submission

## 📁 Submission Contents

This folder contains your Week 2 ETL Pipeline assignments.

### Required Files
- [ ] `etl_pipeline.py` - Main ETL pipeline
- [ ] `data_extractors.py` - Data extraction modules
- [ ] `data_transformers.py` - Data transformation logic
- [ ] `data_loaders.py` - Data loading functions
- [ ] `config.yaml` - Pipeline configuration
- [ ] `tests/` - Unit tests
- [ ] `README.md` - Project documentation (this file)

### Submission Checklist
- [ ] Pipeline handles multiple data sources
- [ ] Error handling and logging implemented
- [ ] Data validation checks included
- [ ] Performance optimization applied
- [ ] Documentation is complete

## 🚀 How to Run

1. **Set up environment**
   ```bash
   pip install apache-airflow pyyaml schedule
   ```

2. **Run ETL pipeline**
   ```bash
   python etl_pipeline.py
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

## 📊 Results Summary

- Successfully built and executed an ETL pipeline using Mage.
- The pipeline loaded the dataset sample_data.csv from the /home/src/data/ directory.
- No errors occurred after fixing the @data_loader decorator and ensuring the correct file path.
- The data was cleaned and passed correctly to the next blocks in the pipeline.
- All blocks in the pipeline were executed step by step without any errors.

## 🎯 Learning Outcomes

- Gained an understanding of how pipeline structures work in Mage.ai.
- Learned how to use the @data_loader decorator to load data from a file.
- Understood how to troubleshoot common issues such as:
     - Block data_loader does not have any decorated functions
     - File not found errors inside the container
     - Docker port allocation errors
- Learned how to access a running Docker container using docker exec and inspect files inside it.
- Improved understanding of how file systems interact between the host and Docker containers.

### Create First Pipeline

1. Click "New pipeline"
2. Name it: `pipeline_1`
3. Click "Create pipeline"

#### Add Data Loader:
1. Click "Add block" → "Data loader"
2. Choose "Python" as the block type
3. Name it: `load_csv_data`
4. Add this code:
```python
from mage_ai.io.file import FileIO

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_file(*args, **kwargs):
    filepath = 'data/sample_data.csv'
    return FileIO().load(filepath)

@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
```
#### Add Transformer:
1. Click "Add block" → "Transformer"
2. Choose "Python" as the block type
3. Name it: `clean_data`
4. Add this code:  
```python
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def clean_data(df, *args, **kwargs):
    """
    Clean data: drop missing and duplicate rows
    """
    df = df.dropna()
    df = df.drop_duplicates()
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The cleaned data is undefined'
    assert len(output) > 0, 'No data left after cleaning'
```
#### Add a Data Exporter:
1. Click "Add block" → "Data exporter"
2. Choose "Python" as the block type
3. Name it: `save_cleaned_data`
4. Add this code:
```python
from mage_ai.io.file import FileIO

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_exporter
def export_data(df, *args, **kwargs):
    """
    Save cleaned data to file
    """
    filepath = '/home/src/data/cleaned_data.csv'
    FileIO().export(df, filepath)
    return df


@test
def test_output(output, *args) -> None:
    assert output is not None, 'Export failed'
```