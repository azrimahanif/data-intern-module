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
