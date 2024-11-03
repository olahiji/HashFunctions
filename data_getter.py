from collections import Counter


def analyze_collisions(phone_numbers):
    num = 17
    # Calculate the remainder of each number modulo 4
    remainders = [int(number) % num for number in phone_numbers]

    # Count the occurrences of each remainder
    remainder_counts = Counter(remainders)

    # Calculate the total number of entries and collisions
    total_entries = len(phone_numbers)
    total_collisions = sum(count - 1 for count in remainder_counts.values() if count > 1)

    # Calculate the collision percentage
    collision_percentage = (total_collisions / total_entries) * 100 if total_entries > 0 else 0

    # Display results
    print("Remainder counts:")
    for i in range(num):
        print(f"{i}: {remainder_counts[i]}")

    print(f"\nTotal entries: {total_entries}")
    print(f"Total collisions: {total_collisions}")
    print(f"Collision percentage: {collision_percentage:.2f}%")

    return remainder_counts, collision_percentage


with open('mcdonalds_hash.txt', 'r') as file:
    phone_numbers = [line.strip() for line in file if line.strip()]
analyze_collisions(phone_numbers)
