import pandas as pd

def transform_data(data, config):
    # 1. Buang kolum yang semua kosong
    data = data.dropna(axis=1, how='all')

    # 2. Buang baris dengan negara tidak sah
    invalid_countries = ['Future Country', 'Invalid Country']
    if 'country' in data.columns:
        data = data[~data['country'].isin(invalid_countries)]

    # 3. Buang baris dengan amaun terlalu besar (lebih 100,000)
    if 'amount' in data.columns:
        data = data[data['amount'] < 100_000]

    # 4. Buang baris dengan rating negatif
    if 'rating' in data.columns:
        data = data[data['rating'] >= 0]

    # 5. Buang baris dengan umur luar biasa (contoh > 120)
    if 'age' in data.columns:
        data = data[(data['age'].isnull()) | (data['age'] <= 120)]

    # 6. Buang email tak valid (jika tiada '@')
    if 'email' in data.columns:
        data = data[data['email'].str.contains('@', na=False)]

    # 7. Optional: Buang baris hampir kosong (<= 3 kolum isi)
    data = data[data.count(axis=1) > 3]

    # 8. Buang baris NaN jika config ada 'dropna'
    if config.get('dropna', False):
        data = data.dropna()

    return data

