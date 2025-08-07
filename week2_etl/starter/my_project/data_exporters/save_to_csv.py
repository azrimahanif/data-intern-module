from mage_ai.io.file import FileIO
from pandas import DataFrame

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_file(df: DataFrame, **kwargs) -> None:
    """
    Export dataframe to a CSV file in the container.

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    filepath = '/home/src/data/cleaned_data.csv'
    FileIO().export(df, filepath)
