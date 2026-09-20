import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, root_mean_squared_error
import argparse
from pathlib import Path
import pingouin as pg

parser = argparse.ArgumentParser(description="Read a data file path.")

# Add the path argument
parser.add_argument(
    "data_path", 
    type=str, 
    help="The path to your input data file (e.g., path/to/data.csv)"
)

# Parse the arguments
args = parser.parse_args()

# read in data path from command line
file_path = Path(args.data_path)
# 1. Load your master merged dataset
# df = pd.read_csv('../data/combined_health_data.csv')
df = pd.read_csv(file_path / "merged_health_data.csv")

# 2. Select variables based on your exact column schema
target_col = ['stress', 'anxiety']
feature_cols = [
    'avg_rmssd', 'lf_hf_ratio',             # HRV Biometrics
    'overall_score_x', 'deep_sleep_in_minutes_x', # Sleep Metrics
    'LIGHTLY_ACTIVE', 'MODERATELY_ACTIVE', 'SEDENTARY', 'VERY_ACTIVE', # Activity Levels
    'avg_oxygen'              # Blood Oxygen Biometrics
]

# 3. Handle missing data (NaN) 
# First, drop rows that don't even have a target stress score logged
df_clean1 = df.dropna(subset=target_col).copy()
df_clean = df_clean1.dropna(subset=['avg_rmssd']).copy()

# Fill missing feature gaps with the mean average of that specific column
for col in feature_cols:
    if df_clean[col].isnull().any():
        df_clean[col] = df_clean[col].fillna(df_clean[col].mean())

# 4. Separate features (X) and target (y)
X = df_clean[feature_cols]
y = df_clean[target_col]

# 5. SCALE THE FEATURES (Crucial for comparing active percentages vs oxygen levels)
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# 6. Calculate the correlation of X against y
# Calculate correlation of all features in X against the target y
correlations = X_scaled.corrwith(y['stress'])

print("\nCorrelations between stress and variables:")
print(correlations)

corr_df = correlations.to_frame(name='correlation_with_stress')

# Save to CSV
corr_df.to_csv(file_path / 'stress_correlations.csv', index_label='variable')

correlations = X_scaled.corrwith(y['anxiety'])
print("\nCorrelations between anxiety and variables:")
print(correlations)

corr_df = correlations.to_frame(name='correlation_with_anxiety')

# Save to CSV
corr_df.to_csv(file_path / 'anxiety_correlations.csv', index_label='variable')

print("Correlation between avg_rmssd and deep_sleep_in_minutes: ",
      X_scaled['avg_rmssd'].corr(X_scaled['deep_sleep_in_minutes_x']))

print("Correlation between avg_rmssd and overall_score: ",
       X_scaled['avg_rmssd'].corr(X_scaled['overall_score_x']))

print("Correlation between avg_rmssd and avg_oxygen: ",
       X_scaled['avg_rmssd'].corr(X_scaled['avg_oxygen']))

data = {
    "Variable Pair": [
        "avg_rmssd vs deep_sleep_in_minutes",
        "avg_rmssd vs overall_score",
        "avg_rmssd vs avg_oxygen"
    ],
    "Correlation": [
        X_scaled['avg_rmssd'].corr(X_scaled['deep_sleep_in_minutes_x']),
        X_scaled['avg_rmssd'].corr(X_scaled['overall_score_x']),
        X_scaled['avg_rmssd'].corr(X_scaled['avg_oxygen'])
    ]
}

df_combined = X_scaled.copy()
df_combined['anxiety'] = y['anxiety']

print("Average RMSSD: ", df_clean['avg_rmssd'])

# Compute pairwise correlations specifically against 'anxiety'
results = pg.pairwise_corr(df_combined, columns=['anxiety'])
# print("Available columns:", results.columns.tolist())

# Filter results so you only see anxiety vs all other X_scaled features
# It automatically provides columns 'CI95%' as a list [lower, upper]
print(results[['X', 'Y', 'r', 'n', 'CI95', 'p_unc']])

# Convert to DataFrame and save to CSV
df_corr = pd.DataFrame(data)
df_corr.to_csv(file_path / "rmssd_correlations.csv", index=False)