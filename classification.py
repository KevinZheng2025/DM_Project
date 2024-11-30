import pandas as pd
import json
import os

# Load the JSON file and create a dictionary mapping move_id to classification
json_file_path = "move_classifications.json"  # Replace with your JSON file path
with open(json_file_path, "r") as file:
    move_classifications = json.load(file)

# Create a mapping of move_id to classification
id_to_classification = {
    move_data.get("move_id"): move_data.get("classification", "unknown")
    for move_name, move_data in move_classifications.items()
}

# Function to classify decisions based on the dataset and preloaded JSON mapping
def classify_decision(row):
    """
    Classify the player's decision as passive or aggressive based on move_id.
    """
    decision = int(row["decision"])  # Ensure decision is an integer
    active_pokemon_index = int(row["p1_curr_active"])  # Ensure active_pokemon_index is an integer

    # Switch decisions (5-10) are always passive
    if decision in range(5, 11):
        return "passive"

    # Move decisions (1-4)
    elif decision in [1, 2, 3, 4]:
        move_column = f"p1_poke{active_pokemon_index}_move{decision}"
        move_id = row.get(move_column, -1)  # Get move_id from the column

        if pd.notna(move_id) and move_id != -1:
            return id_to_classification.get(move_id, "unknown")

    # Default case
    return "unknown"

# Define the directories
train_folder = "test"  # Replace with the path to the train subfolder
classified_folder = "test_classified"

# Create the classified folder if it doesn't exist
if not os.path.exists(classified_folder):
    os.makedirs(classified_folder)

# Iterate over all CSV files in the train folder
for filename in os.listdir(train_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(train_folder, filename)
        
        # Load the dataset
        data = pd.read_csv(file_path)
        
        # Check for null values in the "decision" column
        if data["decision"].isnull().any():
            print(f"Skipped file due to null values in 'decision' column: {filename}")
            continue
        
        # Apply classification logic
        data["decision_type"] = data.apply(classify_decision, axis=1)
        
        # Save the updated dataset in the classified folder
        output_file = os.path.join(classified_folder, filename.replace(".csv", "_classified.csv"))
        data.to_csv(output_file, index=False)

print(f"Classified files saved in '{classified_folder}' folder.")