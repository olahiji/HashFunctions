import re

# Open the file to read phone numbers and store the cleaned versions
with open("mcdonalds_hash.txt", "r") as file:
    phone_numbers = file.readlines()

# Process each line to remove non-numeric characters
cleaned_numbers = [re.sub(r"\D", "", number) for number in phone_numbers]

# Open the file in write mode to overwrite with cleaned numbers
with open("mcdonalds_hash.txt", "w") as file:
    for number in cleaned_numbers:
        file.write(number + "\n")

print("Phone numbers have been reformatted.")