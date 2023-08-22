import os
import json


def scrape_local_folder(folder_path, json_data):
    for entry in os.listdir(folder_path):
        entry_path = os.path.join(folder_path, entry)
        if os.path.isdir(entry_path):
            scrape_local_folder(entry_path, json_data)
        elif entry.endswith('.json'):
            with open(entry_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
                json_data.append(content)
                print("Loaded:", content['id'])

def main():
    folder_path = 'advisory-database/advisories'  # Relative path to the current directory
    all_json_data = []

    script_folder = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.join(script_folder, folder_path)

    scrape_local_folder(full_folder_path, all_json_data)

    json_filename = 'advisory_data.json'
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_json_data, jsonfile, indent=4)

if __name__ == "__main__":
    main()
