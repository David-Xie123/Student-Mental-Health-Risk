import pandas as pd
import matplotlib.pyplot as plt
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
# Load your dataset (replace 'your_file.csv' with your actual file path)
df = pd.read_csv(file_path / 'daily_questions.csv')

# Define the columns you want to convert
timestamp_cols = ['timeStampScheduled', 'timeStampSent', 'timeStampStart', 'timeStampStop']
df['date'] = pd.to_datetime(df['timeStampSent'] + df['timeZoneOffset'], unit='s').dt.date

# Option A: Convert to Local Time using the built-in timeZoneOffset column
for col in timestamp_cols:
    df[col] = pd.to_datetime(df[col] + df['timeZoneOffset'], unit='s')

# Option B: Convert to pure UTC instead (uncomment the lines below if preferred)
# for col in timestamp_cols:
#     df[col] = pd.to_datetime(df[col], unit='s', utc=True)

# Save the updated data to a new CSV file
df.to_csv(file_path / 'converted_daily_questions.csv', index=False)
print(df.head())

# 3. Sort by date to make sure the line connects chronologically
df = df.sort_values('date')

# 4. Create the plot
plt.figure(figsize=(10, 5))
plt.plot(df['date'], df['stress'], marker='o', color='crimson', linewidth=2, label='Stress')

# 5. Format the appearance
plt.title('Stress Levels Over Time', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Date (YYYY-MM-DD)', fontsize=12)
plt.ylabel('Stress Level', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()

# 6. Save the plot
plt.savefig(file_path / "Stress_Level_Over_Time.png", dpi=300, bbox_inches="tight")
