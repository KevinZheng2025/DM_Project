import pandas as pd
import os

winners_file_path = "winners.txt" 
train_folder = "trainMV" 
output_folder = "trainMV_processed"


winners_data = {}
with open(winners_file_path, "r") as f:
    for line in f:
        match_data, result = line.strip().split(" : ")
        players, elos = match_data.split(" ")
        player1, player2, match_id = players.split("-")
        player1_elo, player2_elo = map(int, elos.strip("[]").split(","))
        winner = int(result)

        full_match_id = f"{player1}-{player2}-{match_id}".strip()
        winners_data[full_match_id] = {
            "player1_elo": player1_elo,
            "player2_elo": player2_elo,
            "win": 1 if winner == 1 else 0 
        }


os.makedirs(output_folder, exist_ok=True)


for full_match_id, match_info in winners_data.items():

    csv_filename = f"{full_match_id}.csv"
    csv_path = os.path.join(train_folder, csv_filename)
    output_path = os.path.join(output_folder, csv_filename)


    if os.path.exists(csv_path):
        print(f"Processing {csv_filename}...")


        df = pd.read_csv(csv_path)


        df["player1_elo"] = match_info["player1_elo"]
        df["player2_elo"] = match_info["player2_elo"]
        df["win"] = match_info["win"]

        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {csv_filename}")
    else:
        print(f"File {csv_filename} not found. Skipping...")

print(f"All files have been processed and saved to {output_folder}.")
