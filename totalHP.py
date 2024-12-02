import pandas as pd
import os


input_directory = "test"
output_directory = "testHP" 


os.makedirs(output_directory, exist_ok=True)


def process_csv(file_path, output_path):

    df = pd.read_csv(file_path)
    

    player1_hp_cols = [col for col in df.columns if col.startswith("p1_poke") and col.endswith("hpPercent")]
    player2_hp_cols = [col for col in df.columns if col.startswith("p2_poke") and col.endswith("hpPercent")]


    starting_hp_p1 = df[player1_hp_cols].iloc[0].sum()
    starting_hp_p2 = df[player2_hp_cols].iloc[0].sum()
    
    if starting_hp_p1 != 600 or starting_hp_p2 != 600:
        print(f"Skipping {file_path}: Starting HP for players is not 600.")
        return 

    df['player1_total_hpPercent'] = df[player1_hp_cols].sum(axis=1)
    df['player2_total_hpPercent'] = df[player2_hp_cols].sum(axis=1)
    

    df.to_csv(output_path, index=False)


for file_name in os.listdir(input_directory):
    if file_name.endswith(".csv"):
        input_file_path = os.path.join(input_directory, file_name)
        output_file_path = os.path.join(output_directory, file_name)
        

        process_csv(input_file_path, output_file_path)
        print(f"Processed and saved: {output_file_path}")

print("All files processed.")
