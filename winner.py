import pandas as pd
import os

# Define file paths
master_csv_path = "replays.csv" 
classified_folder = "train_classified"

# Load the master CSV file
master_data = pd.read_csv(master_csv_path)

# Iterate over all classified files in the classified folder
for filename in os.listdir(classified_folder):
    if filename.endswith("_classified.csv"):
        file_path = os.path.join(classified_folder, filename)

        # Load the classified file
        classified_data = pd.read_csv(file_path)

        # Extract the replay name (remove "_classified.csv" from filename)
        replay_name = filename.replace("_classified.csv", "")

        # Find the corresponding row in the master CSV
        match_info = master_data[master_data["Replay_Name"] == replay_name]

        if not match_info.empty:
            # Get Player1 and Winner from the master data
            player1 = match_info.iloc[0]["Player1"]
            winner = match_info.iloc[0]["Winner"]

            # Determine Win column value (1 if Player1 is the Winner, otherwise 0)
            win_value = 1 if player1 == winner else 0

            # Add the Win column with the value for all rows
            classified_data["Win"] = win_value

            # Save the updated classified file
            classified_data.to_csv(file_path, index=False)
        else:
            print(f"Replay name not found in master CSV: {replay_name}")

print("Win column added to all relevant classified files.")
