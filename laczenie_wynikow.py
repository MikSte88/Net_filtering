import json
import os

folder_path = 'Results'
output_file_path = 'Wyniki.json'
combined_data = {}

# Przeszukaj folder i połącz pliki JSON
for filename in os.listdir(folder_path):
    with open(os.path.join(folder_path, filename), 'r') as file:
        file_data = json.load(file)
        combined_data[filename] = file_data

# Zapisz połączone dane do jednego pliku JSON
with open(output_file_path, 'w') as output_file:
    json.dump(combined_data, output_file, indent=2)

print(f"Pliki JSON zostały połączone i zapisane w pliku {output_file_path}.")
