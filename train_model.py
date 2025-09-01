import pandas as pd
import numpy as np
import json
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

print("🔹 Loading dataset...")
df = pd.read_csv("Bengaluru_House_Data.csv")

# Clean dataset
df = df.dropna(subset=['location','size','bath','total_sqft','price'])

# Convert 'size' into BHK (extract number from "2 BHK", "4 Bedroom" etc.)
df['bhk'] = df['size'].apply(lambda x: int(x.split(' ')[0]))

# Convert total_sqft safely
def convert_sqft(x):
    try:
        return float(x)
    except:
        tokens = str(x).split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1]))/2
        return None

df['total_sqft'] = df['total_sqft'].apply(convert_sqft)
df = df.dropna(subset=['total_sqft'])

# Feature Engineering
df = df[['location','total_sqft','bath','bhk','price']]
df['location'] = df['location'].apply(lambda x: x.strip())
location_stats = df['location'].value_counts()
df['location'] = df['location'].apply(lambda x: 'other' if location_stats[x] <= 10 else x)

# One-hot encoding
dummies = pd.get_dummies(df['location'], drop_first=True)
X = pd.concat([df[['total_sqft','bath','bhk']], dummies], axis=1)
y = df['price']

print("🔹 Training model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# Save model
with open("bangalore_home_prices_model.pickle", "wb") as f:
    pickle.dump(model, f)

# Save column info
columns = {
    "data_columns": [col.lower() for col in X.columns],
    "location_columns": [col.lower() for col in dummies.columns]
}
with open("columns.json", "w") as f:
    json.dump(columns, f)

print("✅ Training complete. Files saved: bangalore_home_prices_model.pickle & columns.json")
