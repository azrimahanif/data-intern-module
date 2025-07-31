# visualization_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Customer Dashboard")

# Load cleaned data
df = pd.read_csv("cleaned_data.csv")

# Sidebar filter
country = st.sidebar.selectbox("Select Country", df["country"].dropna().unique())

filtered_df = df[df["country"] == country]

st.write(f"### Customers from {country}")
st.dataframe(filtered_df)

# Plot: Purchase Amount Distribution
st.write("### Purchase Amount Distribution")
fig, ax = plt.subplots()
filtered_df["amount"].hist(bins=20, color="skyblue", edgecolor="black", ax=ax)

# Hiasan carta
ax.set_title("Distribution of Purchase Amounts", fontsize=14)
ax.set_xlabel("Amount Spent", fontsize=12)
ax.set_ylabel("Number of Customers", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.7)

st.pyplot(fig)