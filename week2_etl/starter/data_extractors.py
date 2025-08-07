import pandas as pd

def extract_data(config):
    path = config['path']
    return pd.read_csv(path)
