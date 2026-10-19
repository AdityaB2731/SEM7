
from collections import defaultdict

def mapper(text):
    # Emit (letter, 1) for each alphabetic character
    for char in text.lower():
        if char.isalpha() and char.isascii():
            yield (char, 1)


def reducer(mapped_data):
    counts = defaultdict(int)

    # Group and sum values by key
    for letter, count in mapped_data:
        counts[letter] += count

    return counts


# Input dataset
dataset = """
Hello World!
MapReduce is useful.
HELLO 123
"""

# Map phase
mapped_data = list(mapper(dataset))

print("Mapper Output:")
print(mapped_data)

# Reduce phase
result = reducer(mapped_data)

print("\nCharacter Counts:")
for letter in sorted(result):
    print(f"{letter}: {result[letter]}")
