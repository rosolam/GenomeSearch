import re
import itertools
import decimal
import sys

# Define the base 64 character set
base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def decimal_to_base64(decimal_number, precision=100):
    # Convert the number to an integer representation of its base 64 value
    decimal.getcontext().prec = precision + 50  # Extra precision for accuracy
    number = decimal.Decimal(decimal_number)

    # Separate integer and fractional parts
    integer_part = int(number)
    fractional_part = number - integer_part

    # Convert integer part to base 64
    base64_integer = ''
    if integer_part == 0:
        base64_integer = '0'
    else:
        while integer_part > 0:
            base64_integer = base64_chars[integer_part % 64] + base64_integer
            integer_part //= 64

    # Convert fractional part to base 64
    base64_fractional = ''
    for _ in range(precision):
        fractional_part *= 64
        digit = int(fractional_part)
        base64_fractional += base64_chars[digit]
        fractional_part -= digit
        if fractional_part == 0:
            break

    return base64_integer + '.' + base64_fractional if base64_fractional else base64_integer

def generate_permutations_base64(pattern, triplet_nucleotides):
    # Identify unique characters in the pattern
    used_chars = sorted(set(pattern))
    num_unique_chars = len(used_chars)
    
    # Generate all permutations of the triplet nucleotides for the unique characters
    permutations = itertools.permutations(triplet_nucleotides, num_unique_chars)
    
    nucleotide_patterns = []
    for perm in permutations:
        triplet_mapping = {char: perm[i] for i, char in enumerate(used_chars)}
        triplet_nucleotide_str = ''.join(triplet_mapping[char] for char in pattern)
        nucleotide_patterns.append(triplet_nucleotide_str)
        print(triplet_nucleotide_str)
    
    return nucleotide_patterns

nucleotides = ['A', 'C', 'G', 'T']
triplet_nucleotides = [''.join(triplet) for triplet in itertools.product(nucleotides, repeat=3)]

# Example usage
pi_decimal = '3.14159265358979323846264338327950288419716939937510'
precision = 3
encoded_pi = decimal_to_base64(pi_decimal, precision)
print(triplet_nucleotides)
print(f"Base 64 representation of π with precision {precision}: {encoded_pi}")
permutations = generate_permutations_base64(encoded_pi, triplet_nucleotides)
