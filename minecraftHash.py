import requests

def minecraft_hash(input_string):
    url = f"https://api.mojang.com/users/profiles/minecraft/{input_string.strip()}"

    try:
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if 'id' is in the response data
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


# Load strings from file
strings = []

try:
    with open('key_strings.txt', 'r') as file:
        # Strip newline characters and store in the list
        strings = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("The file 'key_strings.txt' was not found.")

# Loop through each string in the list and call the function
for i in range(len(strings)):
    if strings[i]:  # Check if the string is not empty
        minecraft_hash(strings[i])
