import subprocess

# 1. Define your list of input parameters (e.g., folder paths or file names)
parameters = [
    "1", "2", "4", "5", "6", "7", "8", "10",
    "17", "19", "20",
    "22", "24", "26", "27", "28", "29", "30",
    "32", "33", "34"
]

# 2. Define a list of jobs
scripts = ["correlationAnalysis.py"]

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

