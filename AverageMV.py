import pandas as pd
import os
from collections import defaultdict

# Folder containing the CSV files
input_folder = "trainMV_processed"  # Replace with your folder containing the processed CSV files

# Dictionary to store Elo-based movement value data
elo_data = defaultdict(list)

# Function to calculate the interval group for a given Elo
def get_elo_interval(elo):
    return elo // 100  # Group by 100 intervals (e.g., 1500-1599)

# Process each CSV file in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        csv_path = os.path.join(input_folder, filename)
        
        # Load the CSV file
        df = pd.read_csv(csv_path)

        # Ensure the necessary columns exist
        if "movement_value" in df.columns and "player1_elo" in df.columns and "player2_elo" in df.columns:
            # Group movement values by Elo intervals for both player 1 and player 2
            for _, row in df.iterrows():
                player1_interval = get_elo_interval(int(row["player1_elo"]))
                player2_interval = get_elo_interval(int(row["player2_elo"]))
                elo_data[player1_interval].append((row["player1_elo"], row["movement_value"]))
                elo_data[player2_interval].append((row["player2_elo"], row["movement_value"]))
        else:
            print(f"Skipping {filename}: Required columns not found.")

# Calculate average movement value and dynamic Elo ranges for each interval
elo_summary = []
for interval, values in elo_data.items():
    # Extract all Elo values and their corresponding movement values
    elos, movement_values = zip(*values)
    low = min(elos)
    high = max(elos)
    interval_range = f"{low}-{high}"
    average_movement_value = sum(movement_values) / len(movement_values)
    elo_summary.append((interval_range, average_movement_value))

# Convert results to a DataFrame for easier display and save as CSV
elo_df = pd.DataFrame(elo_summary, columns=["Elo_Range", "Average_Movement_Value"])
elo_df.sort_values(by="Elo_Range", inplace=True)

# Save the results to a CSV file
output_file = "AvgMV.csv"
elo_df.to_csv(output_file, index=False)

print(f"Average movement values by dynamic Elo intervals saved to {output_file}.")
