import pandas as pd
from functools import reduce
import argparse
from pathlib import Path

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
# 1. Load both files
df_stress = pd.read_csv(file_path / 'converted_daily_questions.csv')
df_hrv = pd.read_csv(file_path / 'daily_hrv_summary.csv')
df_sleep = pd.read_csv(file_path / 'daily_sleep.csv')
df_activity = pd.read_csv(file_path / 'daily_categorical_percentages.csv')
df_steps = pd.read_csv(file_path / 'daily_sleep.csv')
df_oxygen = pd.read_csv(file_path / 'daily_oxygen_summary.csv')

data_frames = [df_stress, df_hrv, df_sleep, df_activity, df_steps, df_oxygen]

merged_df = reduce(lambda left, right: pd.merge(left, right, on='date', how='left'), data_frames)

# 5. Export to a final combined CSV file
merged_df.to_csv(file_path / 'merged_health_data.csv', index=False)
