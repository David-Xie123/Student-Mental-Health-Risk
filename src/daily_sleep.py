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
df = pd.read_csv(file_path / 'sleep.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'], format = 'ISO8601')
df['date'] = df['timestamp'].dt.date
df.to_csv(file_path / "daily_sleep.csv", index=False)
