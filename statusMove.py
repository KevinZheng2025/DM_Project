import pandas as pd
import json
import os

json_file_path = "moves_status_value.json"
with open(json_file_path, "r") as file:
    move_data = json.load(file)


def calculate_movement_value(row, previous_p2_hp_percent, previous_p1_hp_percent):

    movement_value = 0.0


    if not pd.isna(previous_p2_hp_percent):
        hp_diff_p2 = (previous_p2_hp_percent - row["player2_total_hpPercent"]) / 100
        movement_value += hp_diff_p2


    if not pd.isna(previous_p1_hp_percent):
        hp_diff_p1 = abs(row["player1_total_hpPercent"] - previous_p1_hp_percent) / 200
        movement_value += hp_diff_p1


    if row["decision"] in [1, 2, 3, 4]:
        active_pokemon_index = int(row["p1_curr_active"])
        move_column = f"p1_poke{active_pokemon_index}_move{int(row['decision'])}"
        move_name = row.get(move_column)


        status_value = move_data.get(move_name, {}).get("statusValue", 0.0)
        movement_value += status_value

    return round(movement_value, 3) 


def process_csv(file_path, output_file_path):

    df = pd.read_csv(file_path)


    df["previous_p2_hp_percent"] = df["player2_total_hpPercent"].shift(1)
    df["previous_p1_hp_percent"] = df["player1_total_hpPercent"].shift(1)


    df["movement_value"] = df.apply(
        lambda row: calculate_movement_value(row, row["previous_p2_hp_percent"], row["previous_p1_hp_percent"]),
        axis=1
    )


    df.to_csv(output_file_path, index=False)
    print(f"Processed file saved to: {output_file_path}")


def process_all_csvs_in_folder(input_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)


    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name)

            process_csv(input_file_path, output_file_path)

    print(f"All files in '{input_folder}' have been processed and saved to '{output_folder}'.")

if __name__ == "__main__":
    train_folder = "testHP" 
    output_folder = "testMV"
    process_all_csvs_in_folder(train_folder, output_folder)
