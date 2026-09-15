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

# 1. Read the CSV file (replace 'your_file.csv' with your actual filename)
# Replace 'timestamp_col' and 'category_col' with your actual column names
df = pd.read_csv(file_path / 'activity_level.csv')

# 2. Ensure the timestamp column is in datetime format
df['timestamp_col'] = pd.to_datetime(df['timestamp'])

# 3. Extract just the date (YYYY-MM-DD)
df['date'] = df['timestamp_col'].dt.date

# 4. Create the daily aggregate table (counts per category per day)
daily_summary = pd.crosstab(df['date'], df['level'], normalize = 'index').round(2)

# 5. Display the final table
# print(daily_summary)

# Optional: Save the aggregated result to a new CSV file
daily_summary.reset_index().to_csv(file_path / 'daily_categorical_percentages.csv', index=False)

