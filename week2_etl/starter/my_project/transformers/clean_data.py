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

