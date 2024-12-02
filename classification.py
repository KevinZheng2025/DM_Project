import pandas as pd
import json
import os

json_file_path = "move_classifications.json"
with open(json_file_path, "r") as file:
    move_classifications = json.load(file)

id_to_classification = {
    move_data.get("move_id"): move_data.get("classification", "unknown")
    for move_name, move_data in move_classifications.items()
}

def classify_decision(row):

    decision = int(row["decision"])  
    active_pokemon_index = int(row["p1_curr_active"])  

    # Switch decisions (5-10) are always passive
    if decision in range(5, 11):
        return "passive"

    # Move decisions (1-4)
    elif decision in [1, 2, 3, 4]:
        move_column = f"p1_poke{active_pokemon_index}_move{decision}"
        move_id = row.get(move_column, -1) 

        if pd.notna(move_id) and move_id != -1:
            return id_to_classification.get(move_id, "unknown")

    # Default case
    return "unknown"


train_folder = "test" 
classified_folder = "test_classified"


if not os.path.exists(classified_folder):
    os.makedirs(classified_folder)


for filename in os.listdir(train_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(train_folder, filename)
        

        data = pd.read_csv(file_path)
        

        if data["decision"].isnull().any():
            print(f"Skipped file due to null values in 'decision' column: {filename}")
            continue
        

        data["decision_type"] = data.apply(classify_decision, axis=1)
        

        output_file = os.path.join(classified_folder, filename.replace(".csv", "_classified.csv"))
        data.to_csv(output_file, index=False)

print(f"Classified files saved in '{classified_folder}' folder.")
