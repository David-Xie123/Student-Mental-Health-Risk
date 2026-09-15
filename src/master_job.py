import subprocess

# 1. Define your list of input parameters (e.g., folder paths or file names)
parameters = [
    "1", "2", "4", "5", "6", "7", "8", "9", "10",
    "11", "13", "15", "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
    "31", "32", "33", "34", "35"
]

# 2. Define a list of jobs
scripts = ["convert_daily_questions.py", "daily_activity.py", "daily_hrv.py",
           "daily_oxygen.py", "daily_sleep.py", "daily_steps.py", "merged_data.py"]

# 3. Automatically loop and run the script for each parameter
for param in parameters:
    print(f"--- Starting run with parameter: {param} ---")
    for script in scripts:
    
        # This mirrors running: python your_script.py [param] in the terminal
        result = subprocess.run(
        ["python", script, "../data/" + param],
        capture_output=True,  # Captures terminal output
        text=True             # Keeps output as a string
    )
    
    # Print the script's output to your master terminal 
    print(result.stdout)
    
    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")

