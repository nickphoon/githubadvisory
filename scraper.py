import os
import requests
import json
from datetime import datetime


def format_datetime(iso_datetime):
    dt = datetime.strptime(iso_datetime, "%Y-%m-%dT%H:%M:%SZ")
    formatted = dt.strftime("%d/%m/%Y %I:%M:%S %p")
    return formatted


def format_affected_data(affected_data):
    formatted_ranges = []
    for entry in affected_data:
        package = entry['package']
        ecosystem = package.get('ecosystem', '')
        name = package.get('name', '')

        if 'ranges' in entry:
            for rng in entry['ranges']:
                events = rng['events']
                introduced = next((event['introduced'] for event in events if 'introduced' in event), '')
                fixed = next((event['fixed'] for event in events if 'fixed' in event), '')

                formatted_range = f"{ecosystem} / {name}: Introduced {introduced}, Fixed {fixed}"
                formatted_ranges.append(formatted_range)
        else:
            formatted_ranges.append(f"{ecosystem} / {name}: No version ranges available")

    return '\n'.join(formatted_ranges)


def fetch_and_save_data(token, path, json_data):
    endpoint = f'https://api.github.com/repos/github/advisory-database/contents/{path}'
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        folder_data = response.json()

        for entry in folder_data:
            if entry['type'] == 'file' and entry['name'].endswith('.json'):
                content_response = requests.get(entry['download_url'], headers=headers)
                if content_response.status_code == 200:
                    content = content_response.json()
                    json_data.append(content)
                    print("Saved:", content['id'])
                else:
                    print("Failed to fetch content for file:", entry['name'], content_response.text)
            elif entry['type'] == 'dir':
                # Recursively fetch files in subdirectories
                fetch_and_save_data(token, entry['path'], json_data)
            
    else:
        print("API request failed:", response.text)


def main():
    token = 'personal token'
    path = 'advisories/github-reviewed'  # Adjust the path as needed

    all_json_data = []

    fetch_and_save_data(token, path, all_json_data)

    json_filename = 'advisory_data.json'
    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(all_json_data, jsonfile, indent=4)

if __name__ == "__main__":
    main()
