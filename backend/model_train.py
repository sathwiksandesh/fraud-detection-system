import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load data
df = pd.read_excel("C:/Users/Rohan/Downloads/credit_risk_data.xlsx")

# Features & target
X = df.drop("is_fraud", axis=1)
y = df["is_fraud"]


# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print(classification_report(y_test, preds))

# Save model
with open("fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")