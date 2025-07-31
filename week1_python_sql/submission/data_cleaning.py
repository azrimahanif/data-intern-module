import pandas as pd
from datetime import datetime

# 1. Baca data asal
df = pd.read_csv("data.csv")

# 2. Buang baris yang kosong semua atau critical field kosong
df = df.dropna(how="all")
df = df.dropna(subset=["customer_id", "customer_name", "email"])

# 3. Buang email duplicate (guna email unik)
df = df.drop_duplicates(subset="email", keep="first")

# 4. Tukar column date ke datetime
df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
df["last_purchase"] = pd.to_datetime(df["last_purchase"], errors="coerce")

# 5. Buang baris yang tarikh signup atau last_purchase ke masa depan
today = datetime.today()
df = df[(df["signup_date"] <= today) & (df["last_purchase"] <= today)]

# 6. Buang nilai umur pelik (cth: kosong, negatif atau lebih 100)
df = df[pd.to_numeric(df["age"], errors="coerce").notnull()]
df["age"] = df["age"].astype(int)
df = df[(df["age"] > 0) & (df["age"] <= 100)]

# 7. Buang amount negatif
df = df[pd.to_numeric(df["amount"], errors="coerce").notnull()]
df["amount"] = df["amount"].astype(float)
df = df[df["amount"] >= 0]

# 8. Buang negara yang tak valid
valid_countries = ["USA", "UK", "Canada", "Australia", "Spain"]
df = df[df["country"].isin(valid_countries)]

# 9. Simpan data bersih ke file baru
df.to_csv("cleaned_data.csv", index=False)

print(f"✅ Data cleaned. File saved as 'cleaned_data.csv' Total Cleaned: {len(df)}")
