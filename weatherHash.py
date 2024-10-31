import requests
from datetime import datetime

def load_zip_codes(file_path="zipcodes.txt"):
    with open(file_path, "r") as file:
        return {line.strip() for line in file}

def get_closest_zip(zip_code, valid_zip_codes):
    """
    GPT - Find the numerically closest ZIP code from the valid list.
    """
    zip_code_int = int(zip_code)
    closest_zip = min(valid_zip_codes, key=lambda valid_zip: abs(int(valid_zip) - zip_code_int))
    return closest_zip

def get_coordinates_from_zip(zip_code, api_key):
    try:
        url = f"https://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data["lat"], data["lon"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")
    return None, None

def base26ToBase10(input_string):
    input_string = input_string.lower()
    base10_num = 0
    length = len(input_string)
    for i, char in enumerate(input_string):
        position_value = ord(char) - ord('a')
        base10_num += position_value * (26 ** (length - i - 1))
    return base10_num

def stringToZip(input_string):
    zip_min, zip_max = 501, 99950  # Valid U.S. ZIP code range
    base26_num = base26ToBase10(input_string)
    # GPT - constrain and use zfill to make 5 characters
    zip_code = zip_min + (base26_num % (zip_max - zip_min + 1))
    return str(zip_code).zfill(5)

def get_unix_timestamp(date_str: str) -> int:
    # GPT - convert date to UNIX for API
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())

def get_historical_temperature(input_string: str, api_key: str, valid_zip_codes):
    zip_code = stringToZip(input_string)
    print(f"Generated ZIP code: {zip_code}")

    if zip_code not in valid_zip_codes:
        closest_zip = get_closest_zip(zip_code, valid_zip_codes)
        if closest_zip:
            print(f"Using closest valid ZIP code: {closest_zip}")
            zip_code = closest_zip
        else:
            return f"No valid ZIP code found close to {zip_code}."

    lat, lon = get_coordinates_from_zip(zip_code, api_key)
    if lat is None or lon is None:
        return f"Could not retrieve coordinates for ZIP code {zip_code}."

    start = get_unix_timestamp("2024-5-20 00:00:00")
    end = get_unix_timestamp("2024-5-20 23:59:00")

    url = (
        f"https://history.openweathermap.org/data/2.5/history/city?"
        f"lat={lat}&lon={lon}&type=hour&start={start}&end={end}&cnt=1&appid={api_key}&units=imperial"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    if 'list' not in data or len(data['list']) == 0:
        return f"No historical weather data available for ZIP code {zip_code} on May 20."


    temp = round(data['list'][0]['main']['temp'])
    return temp

api_key = "0a590db06d52de92cc553f15b7b743c7"

valid_zip_codes = load_zip_codes()

random_string = "zipcode"
print(get_historical_temperature(random_string, api_key, valid_zip_codes))
