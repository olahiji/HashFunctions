import requests
def base26ToBase10(input_string): # Made by ChatGPT
    # Convert the string to lowercase to handle case insensitivity
    input_string = input_string.lower()
    base10_num = 0
    length = len(input_string)
    # Iterate over each character in the string
    for i, char in enumerate(input_string):
        # Calculate the position value from the rightmost character
        position_value = ord(char) - ord('a')
        # Multiply the character's value by 26 raised to its position from the right
        base10_num += position_value * (26 ** (length - i - 1))
    return base10_num
def stringToCoordinates(input_string):
    lat_min, lat_max = 29.501657, 30.038077
    lon_min, lon_max = -95.707054, -95.107910

    # Split the input string into two parts: even-indexed and odd-indexed characters
    lat_string = input_string[::2]  # Characters at even indices
    lon_string = input_string[1::2]  # Characters at odd indices

    # Convert each part to a base 26 number
    lat_base26 = base26ToBase10(lat_string)
    lon_base26 = base26ToBase10(lon_string)

    # Normalize each base 26 number independently
    max_lat_value = 26 ** len(lat_string) - 1 if len(lat_string) > 0 else 1
    max_lon_value = 26 ** len(lon_string) - 1 if len(lon_string) > 0 else 1

    lat_normalized = lat_base26 / max_lat_value if max_lat_value > 0 else 0
    lon_normalized = lon_base26 / max_lon_value if max_lon_value > 0 else 0

    # Convert the normalized values to latitude and longitude within the specified ranges
    lat = (lat_normalized * (lat_max - lat_min)) + lat_min
    lon = (lon_normalized * (lon_max - lon_min)) + lon_min

    # Format to 6 decimal places explicitly
    lat = format(lat, ".6f")
    lon = format(lon, ".6f")

    return lat, lon
def find_nearest_mcdonalds(lat, lon):

    api_url = "http://localhost:3000/nearest-mcdonalds"
    params = {
        'latitude': lat,
        'longitude': lon
    }
    response = requests.get(api_url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def display_nearby_stores(data):
    # Check if 'nearByStores' is present in the response
    if 'nearByStores' in data:
        stores = data['nearByStores']
        if stores:
            print(f"Found {len(stores)} nearby McDonald's locations:\n")
            for store in stores:
                print(f"Store Number: {store['storeNumber']}")
                print(f"Status: {store['storeStatus']}")
                print(f"Phone Number: {store['phoneNumber']}")
                print(f"Address: {store['addressLine1']}, {store['addressLine3']}, {store['subDivision']}, {store['postCode']}")
                print(f"Geo Coordinates: Latitude={store['geoPoint']['latitude']}, "
                      f"Longitude={store['geoPoint']['longitude']}")
                print("https://www.google.com/maps/search/"+f"{store['geoPoint']['latitude']}"+","+f"{store['geoPoint']['longitude']}")
        else:
            print("No nearby McDonald's locations found.")
    else:
        print("Invalid response structure.")


def main():
    # Input string from the user
    #input_string = input("Enter a string to hash and find the nearest McDonald's: ")

    # Convert string to coordinates
    #lat, lon = stringToCoordinates(input_string)
    #print(f"Coordinates derived from the hash: Latitude={lat}, Longitude={lon}")

    # Attempt to find the nearest McDonald's using the Node.js API
    #try:
    #    nearest_mcdonalds = find_nearest_mcdonalds(lat, lon)
    #    display_nearby_stores(nearest_mcdonalds)
    #except Exception as e:
    #    print("Failed to find the nearest McDonald's:", e)
    process_key_strings()

def process_key_strings(): # Made by ChatGPT
    try:
        # Read the contents of the key_strings.txt file
        with open('key_strings.txt', 'r') as file:
            key_strings = [line.strip() for line in file if line.strip()]


        # List to store the last two digits of phone numbers
        results = []

        # Process each key string
        for key in key_strings:
            lat, lon = stringToCoordinates(key)
            nearest_mcdonalds=find_nearest_mcdonalds(lat, lon)
            stores = nearest_mcdonalds['nearByStores']
            for store in stores:
                phone_number = store['phoneNumber']
            last_two_digits = phone_number[-2:]
            results.append(last_two_digits)


        # Write the results to the hash_results.txt file
        with open('mcdonalds_hash.txt', 'w') as output_file:
            for result in results:
                output_file.write(result + '\n')

        print("Processing complete. Results saved to hash_results.txt.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()