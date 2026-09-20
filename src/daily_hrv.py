import pandas as pd
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
# Load, format, and aggregate data
df = pd.read_csv(file_path / 'hrv.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date

def p25(x):
  return x.quantile(0.25)


daily_summary = df.groupby('date').agg(
    avg_rmssd=('rmssd', 'mean'),
    min_rmssd=('rmssd', 'min'),
    max_rmssd=('rmssd', 'max'),
    percentile_25=('rmssd', p25),
    avg_lf=('low_frequency', 'mean'),
    avg_hf=('high_frequency', 'mean'),
    lf_hf_ratio=('low_frequency', lambda x: (x / df.loc[x.index, 'high_frequency']).mean()),
    avg_coverage=('coverage', 'mean')
).reset_index()

# Export straight to a fresh CSV file
daily_summary.to_csv(file_path / 'daily_hrv_summary.csv', index=False)

