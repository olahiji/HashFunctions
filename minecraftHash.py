import requests

# GPT - Check if the variable is a digit
def is_number(var):
    return var.isdigit()

def sigma(input_id):
    sum_digits = 0
    for char in input_id:
        if is_number(char):
            sum_digits += int(char)
    return sum_digits

def minecraft_hash(input_string):
    url = f"https://api.mojang.com/users/profiles/minecraft/{input_string.strip()}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'id' in data:
            id = data['id']
            return id
        else:
            print(f"Error: 'id' not found for input '{input_string.strip()}'")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for '{input_string.strip()}': {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for '{input_string.strip()}': {req_err}")
    except ValueError:
        print(f"Error: Could not parse JSON response for '{input_string.strip()}'")

    return None

strings = []

try:
    with open('key_strings.txt', 'r') as file:
        strings = [line.strip() for line in file.readlines()]
except FileNotFoundError:
    print("The file 'key_strings.txt' was not found.")

for string in strings:
    if string:
        string_id = minecraft_hash(string)
        if string_id:
            print(f"Sigma for '{string}': {sigma(string_id)}")
