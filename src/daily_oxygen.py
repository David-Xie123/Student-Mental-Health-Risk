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
# Load and prepare your data
df = pd.read_csv(file_path / 'oxygen.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['date'] = df['timestamp'].dt.date

daily_summary = df.groupby('date').agg(
    avg_oxygen=('value', 'mean'),
    min_oxygen=('value', 'min'),
    max_oxygen=('value', 'max'),
    median_oxygen=('value', 'median')
).reset_index()

# Export to a fresh CSV file
daily_summary.to_csv(file_path / 'daily_oxygen_summary.csv', index=False)

