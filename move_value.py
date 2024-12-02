import json


entry_hazards_status_values = {
    "Ceaseless Edge": 0.6,
    "Spikes": 0.5,
    "Stealth Rock": 0.7,
    "Sticky Web": 0.4,
    "Stone Axe": 0.65,
    "Toxic Spikes": 0.55,
}


input_file_path = "original_with_status_value.json"  # Replace with your original file path
output_file_path = "updated_original_with_status_value.json"  # Path to save the updated file


with open(input_file_path, "r") as file:
    move_data = json.load(file)


for move_name, status_value in entry_hazards_status_values.items():
    move_key = move_name.lower().replace(" ", "")
    if move_key in move_data:
        move_data[move_key]["statusValue"] = status_value

with open(output_file_path, "w") as file:
    json.dump(move_data, file, indent=4)

print(f"Updated JSON file saved as: {output_file_path}")
