import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error

# 1. Load your master merged dataset
df = pd.read_csv('merged_health_data.csv')

# 2. Select variables based on your exact column schema
target_col = 'stress'
feature_cols = [
    'avg_rmssd', 'lf_hf_ratio',             # HRV Biometrics
    'overall_score_x', 'deep_sleep_in_minutes_x', # Sleep Metrics
    'LIGHTLY_ACTIVE', 'MODERATELY_ACTIVE', 'SEDENTARY', 'VERY_ACTIVE', # Activity Levels
    'avg_oxygen', 'min_oxygen'              # Blood Oxygen Biometrics
]

# 3. Handle missing data (NaN) 
# First, drop rows that don't even have a target stress score logged
df_clean = df.dropna(subset=[target_col]).copy()

# Fill missing feature gaps with the mean average of that specific column
for col in feature_cols:
    if df_clean[col].isnull().any():
        df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

# 4. Separate features (X) and target (y)
X = df_clean[feature_cols]
y = df_clean[target_col]

# 5. Split into Training (80%) and Testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. SCALE THE FEATURES (Crucial for comparing active percentages vs oxygen levels)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 7. Initialize and train the Linear Regression Model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# 8. Predict and evaluate performance
y_pred = model.predict(X_test_scaled)

print("--- Model Performance Summary ---")
print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred):.2f}")
print(f"R-squared Score (R²): {r2_score(y_test, y_pred):.2f}")
print(f"Root Mean Squared Error: {root_mean_squared_error(y_test, y_pred):.2f}")

print("\n--- Standardized Feature Impact (Sorted by Strength) ---")
# Combining features and weights to sort them by absolute impact strength
coefficients = zip(feature_cols, model.coef_)
sorted_coefficients = sorted(coefficients, key=lambda x: abs(x[1]), reverse=True)

for feature, coef in sorted_coefficients:
    direction = "Increases Stress" if coef > 0 else "Decreases Stress"
    print(f"{feature:<25}: {coef:+.4f} ({direction})")

print(f"\nBaseline Constant (Intercept): {model.intercept_:.2f}")
