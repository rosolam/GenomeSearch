import re
import itertools
import decimal
import sys

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def read_genome_from_file(file_path):
    with open(file_path, 'r') as file:
        genome_sequence = ''.join(line.strip() for line in file if not line.startswith('>'))
    return genome_sequence

def encode_base4(number, precision=100):
    # Set precision for decimal operations
    decimal.getcontext().prec = precision + 10  # Extra precision to ensure accuracy

    # Split the number into its integer and fractional parts
    number = decimal.Decimal(number)
    integer_part = int(number)
    fractional_part = number - integer_part

    # Convert the integer part to base 4
    base4_integer = ''
    if integer_part == 0:
        base4_integer = '0'
    else:
        while integer_part > 0:
            base4_integer = str(integer_part % 4) + base4_integer
            integer_part //= 4

    # Convert the fractional part to base 4 with extra precision
    base4_fractional = ''
    for _ in range(precision + 10):  # Adding extra digits for accuracy
        fractional_part *= 4
        digit = int(fractional_part)
        base4_fractional += str(digit)
        fractional_part -= digit
        if fractional_part == 0:
            break

    # Truncate to the requested precision
    #base4_fractional = base4_fractional[:precision]

    return base4_integer + '.' + base4_fractional if base4_fractional else base4_integer

def generate_permutations_base4(pattern):
    # Generate all permutations of A, T, C, G
    nucleotides = ['A', 'T', 'C', 'G']
    permutations = list(itertools.permutations(nucleotides))

    # Create search patterns for each permutation
    patterns = []
    for perm in permutations:
        trans_table = str.maketrans('0123', ''.join(perm))
        patterns.append((pattern.translate(trans_table), perm))
    return patterns

""" def generate_permutations_base64(pattern, triplet_nucleotides):
    used_chars = sorted(set(pattern))  # Get unique characters used in the pattern and sort them
    # Generate all permutations of the 64 triplet nucleotides
    permutations = itertools.permutations(triplet_nucleotides, len(used_chars))
    
    nucleotide_patterns = []
    for perm in permutations:
        triplet_mapping = {char: perm[i] for i, char in enumerate(used_chars)}
        triplet_nucleotide_str = ''.join(triplet_mapping[char] for char in pattern)
        nucleotide_patterns.append(triplet_nucleotide_str)
    
    return nucleotide_patterns """

""" def encode_base64(decimal_number, precision=100):
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

    return base64_integer + '.' + base64_fractional if base64_fractional else base64_integer """

""" def create_regex_pattern(pattern, use_wildcard):
    if use_wildcard:
        # Create a regex pattern that matches the specified nucleotides or 'N' in the genome
        regex_pattern = ''.join([f"[{base}N]" for base in pattern])
    else:
        # Create a regex pattern that matches the specified nucleotides exactly
        regex_pattern = pattern
    # Compile the regex pattern with case insensitivity
    regex = re.compile(regex_pattern, re.IGNORECASE)
    return regex

def count_non_n_matches(match, pattern):
    # Count the number of non-'N' matches in the match
    match_sequence = match.group()
    non_n_count = sum(1 for i in range(len(pattern)) if match_sequence[i].upper() == pattern[i].upper())
    return non_n_count

def search_genome_regex(genome_sequence, search_pattern, min_non_n_matches, use_wildcard=True):
    # Create the regex patterns from the search pattern and its reverse
    regex = create_regex_pattern(search_pattern, use_wildcard)
    reversed_pattern = search_pattern[::-1]
    regex_reversed = create_regex_pattern(reversed_pattern, use_wildcard)

    # Find all matches in the genome sequence for both patterns
    matches = regex.finditer(genome_sequence)
    matches_reversed = regex_reversed.finditer(genome_sequence)

    def extract_context(match):
        start, end = match.start(), match.end()
        before = genome_sequence[max(0, start-10):start]
        after = genome_sequence[end:end+10]
        matched_value = genome_sequence[start:end]
        return start, end, before, matched_value, after

    # Filter matches based on the required number of non-'N' matches
    if use_wildcard:
        valid_matches = [extract_context(match) for match in matches if count_non_n_matches(match, search_pattern) >= min_non_n_matches]
        valid_matches_reversed = [extract_context(match) for match in matches_reversed if count_non_n_matches(match, reversed_pattern) >= min_non_n_matches]
        return valid_matches + valid_matches_reversed
    else:
        return [extract_context(match) for match in matches] + [extract_context(match) for match in matches_reversed] """

def search_genome(genome_sequence, search_pattern):
    search_pattern_upper = search_pattern.upper()
    reversed_pattern_upper = search_pattern_upper[::-1]
    
    start = 0
    matches = []

    # Function to find matches and add to the list
    def find_matches(pattern):
        nonlocal start
        start = 0
        while True:
            start = genome_sequence.find(pattern, start)
            if start == -1:
                break
            end = start + len(pattern)
            preceding = genome_sequence[max(0, start-10):start]
            matching = genome_sequence[start:end]
            following = genome_sequence[end:end+10]
            matches.append((start, end, preceding, matching, following))
            start += 1  # Move past the last match

    # Find matches for both the pattern and its reverse
    find_matches(search_pattern_upper)
    find_matches(reversed_pattern_upper)

    return matches

def convert_to_numeric_version(sequence, perm):
    trans_table = str.maketrans(''.join(perm), '0123')
    return sequence.translate(trans_table)

def process_floats_and_search_genome(search_numbers, genome_sequence, min_non_n_matches, use_wildcard, precision, encoding, drop_int):

    nucleotides = ['A', 'C', 'G', 'T']
    #triplet_nucleotides = [''.join(triplet) for triplet in itertools.product(nucleotides, repeat=3)] if encoding == 'base64' else None
    genome_sequence_upper = genome_sequence.upper() # needed for nonregex case insensitive search

    for search_number in search_numbers:
        if encoding == 'base4':
            full_pattern = encode_base4(search_number, 50)
            pattern = full_pattern[:precision]
            if drop_int:
                int_part, decimal_part = full_pattern.split('.')
                pattern = decimal_part[:precision]
                next10pattern = decimal_part[precision:precision + 10]
                print(f"Base 4 representation of {search_number}: {full_pattern} search pattern: {int_part}[{pattern}]{next10pattern}")
            else:
                pattern = full_pattern.replace('.', '')[:precision]
                next10pattern = full_pattern.replace('.', '')[precision:precision + 10]
                print(f"Base 4 representation of {search_number}: {full_pattern} search pattern: [{pattern}]{next10pattern}")
            nucleotide_patterns = generate_permutations_base4(pattern)
        elif encoding == 'base64':
            """ pattern = encode_base64(search_number)
            print(f"Base 64 representation of {search_number}: {pattern}")
            if(drop_int == True):
                _, pattern = pattern.split('.')
                print(pattern)
            else:
                pattern = pattern.replace('.', '')
            nucleotide_patterns = generate_permutations_base64(pattern, triplet_nucleotides) """

        for i, (search_pattern, perm) in enumerate(nucleotide_patterns, 1):
            mapping = ', '.join(f'{i}={n}' for i, n in zip('0123', perm))
            #print(f"Searching Pattern {i}: {search_pattern} (Mapping: {mapping})")
            #matches = search_genome(genome_sequence, search_pattern, min_non_n_matches, use_wildcard)
            matches = search_genome(genome_sequence_upper, search_pattern)
            for match in matches:
                start, end, preceding, matching, following = match
                numeric_preceding = convert_to_numeric_version(preceding, perm)
                numeric_matching = convert_to_numeric_version(matching, perm)
                numeric_following = convert_to_numeric_version(following, perm)
                print(f"Match found: Pattern {i} {search_pattern} (Mapping: {mapping}) {start} to {end} {preceding}[{matching}]{following} {numeric_preceding}[{numeric_matching}]{numeric_following}")

print("Loading Genome...")
genome_sequence = read_genome_from_file('GCF_000001405.40_GRCh38.p14_genomic.fna')
print("Genome loaded!")

search_numbers = [
    decimal.Decimal('3.14159265358979323846264338327950288419716939937510'),  # Pi (π)
    decimal.Decimal('6.28318530717958647692528676655900576839433879875020'),  # Tau
    decimal.Decimal('2.71828182845904523536028747135266249775724709369995'),  # Euler's Number (e)
    decimal.Decimal('1.61803398874989484820458683436563811772030917980576'),  # Golden Ratio (φ)
    decimal.Decimal('4.66920160910299067185320382046620161725818557747576'),  # Feigenbaum Constant (δ)
    decimal.Decimal('2.50290787509589282228390287321821578638127137672714'),  # Feigenbaum Constant (α)
    decimal.Decimal('1.20205690315959428539973816151144999076498629234050'),  # Apéry's Constant (ζ(3))
    decimal.Decimal('2.68545200106530644530971483548179569382038229399446'),  # Khinchin's Constant
    decimal.Decimal('1.28242712910062263687534256886979172776768892732500'),  # Glaisher-Kinkelin Constant (A)
    decimal.Decimal('0.91596559417721901505460351493238411077414937428167'),  # Catalan's Constant (G)
    decimal.Decimal('1.90216058310401225355083740436407981021334353001897'),  # Brun's Constant for Twin Primes (B2)
    decimal.Decimal('1.324717957244746025960908854478097340734404056901733'), # Plastic Number (ρ)
    decimal.Decimal('1.41421356237309504880168872420969807856967187537694'),  # Square Root of 2 (√2)    
    decimal.Decimal('0.57721566490153286060651209008240243104215933593992'),  # Euler-Mascheroni Constant (γ)
    decimal.Decimal('2.29558714939263807403429804918949039'),                  # Embree-Trefethen Constant
    decimal.Decimal('1.303577269034296391257099112152551890730702504659939'),  # Conway's Constant (λ)
    decimal.Decimal('0.62432998854355087099293638310083724'),                  # Golomb-Dickman Constant (δ)
    decimal.Decimal('0.2614972128476427837554268386086958590515666482617'),    # Meissel-Mertens Constant (M)
    decimal.Decimal('1.705211140105367764288551453434508160477'),              # Niven's Constant
    decimal.Decimal('0.235711131719232931374143179454494'),                    # Copeland-Erdős Constant
    decimal.Decimal('0.1234567891011121314151617181920'),                      # Champernowne Constant
    decimal.Decimal('0.110001000000000000000001000'),                          # Liouville's Constant
    decimal.Decimal('0.30366300289873265859744812190155623'),                  # Gauss-Kuzmin-Wirsing Constant
    decimal.Decimal('2.807770242028519365221501186557772932130349804086'),     # Fransén-Robinson Constant
    decimal.Decimal('1.30637788386308069046861449260260571')                   # Mills' Constant
] 

# Calculate and insert the reciprocal of each value
i = 0
while i < len(search_numbers):
    original_value = search_numbers[i]
    reciprocal_value = decimal.Decimal(1) / original_value
    search_numbers.insert(i + 1, reciprocal_value)
    i += 2  # Move to the next original value

# Print the updated search_numbers list
for number in search_numbers:
    print(number)

process_floats_and_search_genome(search_numbers, genome_sequence, 0, False, 19, 'base4', True)