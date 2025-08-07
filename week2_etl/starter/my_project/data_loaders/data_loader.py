import pandas as pd
from mage_ai.data_preparation.decorators import data_loader
from mage_ai.data_preparation.shared.secrets import get_secret_value

@data_loader
def load_data(*args, **kwargs):
    file_path = '/home/src/data/sample_data.csv'  # Pastikan file ini betul-betul wujud dalam container
    df = pd.read_csv(file_path)
    return df


