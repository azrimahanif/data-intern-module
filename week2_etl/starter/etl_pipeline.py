import yaml
from data_extractors import extract_data
from data_transformers import transform_data
from data_loaders import load_data

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config()

    # Extract
    data = extract_data(config['extract'])

    # Transform
    data = transform_data(data, config['transform'])

    # Load
    load_data(data, config['load'])

    print("ETL pipeline done.")

if __name__ == "__main__":
    main()
