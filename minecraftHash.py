import requests

def minecraft_hash(input_string):
    url = f"https://api.mojang.com/users/profiles/minecraft/{input_string.strip()}"

    try:
        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        if 'id' in data:
            print(f"ID for '{input_string.strip()}': {data['id']}")
        else:
            print(f"Error: 'id' not found for input '{input_string.strip()}'")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for '{input_string.strip()}': {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for '{input_string.strip()}': {req_err}")
    except ValueError:
        print(f"Error: Could not parse JSON response for '{input_string.strip()}'")


strings = []

try:
    with open('key_strings.txt', 'r') as file:
        strings = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("The file 'key_strings.txt' was not found.")

for i in range(len(strings)):
    if strings[i]:
        minecraft_hash(strings[i])
