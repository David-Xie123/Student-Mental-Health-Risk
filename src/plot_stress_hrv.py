import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import matplotlib.dates as mdates

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

df = pd.read_csv(file_path / "merged_health_data.csv")

df['date'] = pd.to_datetime(df['date'])

fig, ax = plt.subplots()

# ax.figure(figsize=(10, 5))
line1 = ax.plot(df['date'], df['stress'], marker='o', color='crimson', linewidth=2, label='Stress')
ax2 = ax.twinx()  # <-- This creates the secondary Y-axis
line2 = ax2.plot(df['date'], df['avg_rmssd'], marker = 'o', linestyle = '--', color="black", label="RMSSD")
ax2.set_ylabel("RMSSD")
ax2.tick_params(axis='y') # Color the tick marks to match
# ax.plot(df['date'], df['avg_rmssd'], marker='o', linestyle='--', label = "RMSSD")

# 5. Format the appearance
ax.set_title('Stress and RMSSD Levels Over Time', fontsize=14, fontweight='bold', pad=15)
# ax2.set_title('Average RMSSD Over Time', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Date (YYYY-MM-DD)', fontsize=12)
ax.set_ylabel('Stress Level', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.6)
# ax.xticks(rotation=45)
plt.tight_layout()
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# 2. Combine them into a single legend box
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))

# Format how the date looks (e.g., 2026-09)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()
plt.show()

# 6. Save the plot
plt.savefig(file_path / "Stress_Level_And_HRV_Over_Time.png", dpi=300, bbox_inches="tight")
