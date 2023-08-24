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

def scrape(folder_path):
    folder_name = folder_path.split("/")
    
    if "github" in folder_name[-1]:
        final_folder_name = "reviewed"
    else:
        final_folder_name = folder_name[-1]
    script_folder = os.path.dirname(os.path.abspath(__file__))
    full_folder_path = os.path.join(script_folder, folder_path)
    
    for entry in os.listdir(full_folder_path):
        all_json_data = []
        json_filename = final_folder_name+'advisory_data'+entry+'.json' 
        new_path = os.path.join(full_folder_path,entry)
        
        scrape_local_folder(new_path, all_json_data)
        with open(json_filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(all_json_data, jsonfile, indent=4)

    single_json_data = []
    single_json_filename = final_folder_name + 'advisory_data.json'
     
    for file in os.listdir(script_folder):
        if file.startswith(final_folder_name+ "advisory_data2"):
            file_path = os.path.join(script_folder, file)
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                single_json_data.append(data)
    
    with open(single_json_filename, "w") as output_json:
        json.dump(single_json_data, output_json, indent=4)


def main():
    github_reviewed = './MyFileName/advisory-database-main/advisories/github-reviewed'  # Relative path to the current directory
    
    unreviewed = './MyFileName/advisory-database-main/advisories/unreviewed'
    
    scrape(github_reviewed)
    scrape(unreviewed)
    

if __name__ == "__main__":
    main()
