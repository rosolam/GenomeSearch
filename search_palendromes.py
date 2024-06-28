import re
import itertools
import decimal
import sys

def read_genome_from_file(file_path):
    with open(file_path, 'r') as file:
        genome_sequence = ''.join(line.strip() for line in file if not line.startswith('>'))
    return genome_sequence

def is_repeated_sequence(substring):
    length = len(substring)
    for i in range(1, length // 2 + 1):
        if length % i == 0 or length % i >= 0:  # Check if the length is a multiple or can be split with trailing value
            unit = substring[:i]
            repetitions = length // i
            if unit * repetitions + unit[:length % i] == substring:
                return True
    return False

def longest_palindromic_substring(genome_sequence):
    n = len(genome_sequence)
    if n == 0:
        return ""

    # Function to expand around the center and find palindromes
    def expand_around_center(left, right):
        while left >= 0 and right < n and genome_sequence[left] == genome_sequence[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    start, end = 0, 0
    progress_step = n // 10
    next_progress = progress_step

    for i in range(n):
        # Print progress at each 10%
        if i >= next_progress:
            print(f"Progress: {i * 100 // n}% complete")
            next_progress += progress_step

        # Check for odd-length palindromes
        l1, r1 = expand_around_center(i, i)
        # Check for even-length palindromes
        l2, r2 = expand_around_center(i, i + 1)

        # Check and update the longest palindrome found for odd-length palindromes
        substring = genome_sequence[l1:r1 + 1]
        if 'N' not in substring and not is_repeated_sequence(substring):
            if r1 - l1 > end - start:
                start, end = l1, r1
                print(f"New longest palindromic substring: {substring}")
            elif r1 - l1 == end - start and substring != genome_sequence[start:end + 1]:
                print(f"Equal longest palindromic substring: {substring}")

        # Check and update the longest palindrome found for even-length palindromes
        substring = genome_sequence[l2:r2 + 1]
        if 'N' not in substring and not is_repeated_sequence(substring):
            if r2 - l2 > end - start:
                start, end = l2, r2
                print(f"New longest palindromic substring: {substring}")
            elif r2 - l2 == end - start and substring != genome_sequence[start:end + 1]:
                print(f"Equal longest palindromic substring: {substring}")

    return genome_sequence[start:end + 1]


print("Loading Genome...")
genome_sequence = read_genome_from_file('GCF_000001405.40_GRCh38.p14_genomic.fna')
genome_sequence_upper = genome_sequence.upper() # needed for nonregex case insensitive search

longest_palindrome = longest_palindromic_substring(genome_sequence_upper)
print(f"Done - Longest palindromic substring: {longest_palindrome}")
