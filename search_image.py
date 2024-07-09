import numpy as np
from PIL import Image
from math import sqrt, ceil

# Map nucleotides to grayscale values
NUCLEOTIDE_TO_GRAYSCALE = {
    'A': 64,    # Black
    'C': 128,   # Dark Gray
    'G': 192,  # Light Gray
    'T': 255,  # White
}

def read_genome_from_file(file_path):
    with open(file_path, 'r') as file:
        genome_sequence = ''.join(line.strip() for line in file if not line.startswith('>'))
    return genome_sequence

def save_genome_as_tiff(genome, row_size, file_name):

    # Determine the number of rows needed
    num_rows = (len(grayscale_values) + row_size - 1) // row_size

    # Pad the grayscale values to make a complete rectangle
    padded_length = num_rows * row_size
    grayscale_values.extend([0] * (padded_length - len(grayscale_values)))

    # Reshape the list into a 2D array
    grayscale_array = np.array(grayscale_values, dtype=np.uint8).reshape((num_rows, row_size))

    # Convert the numpy array to a PIL Image
    image = Image.fromarray(grayscale_array)

    # Save the image as a TIFF file
    image.save(file_name, format='TIFF')

print("Loading Genome...")
genome_sequence = read_genome_from_file('GCF_000001405.40_GRCh38.p14_genomic.fna')
genome_sequence = genome_sequence.upper()
print("Genome loaded!")

print("Converting to grayscale...")
# Convert the genome string to a list of grayscale values
grayscale_values = [NUCLEOTIDE_TO_GRAYSCALE.get(nucleotide, 0) for nucleotide in genome_sequence]

row_sizes = [64, 256, 1024, 4096, 16384]  # Example row sizes
for row_size in row_sizes:
    print(f"creating image with row size of {row_size}...")
    save_genome_as_tiff(grayscale_values, row_size, f'genome_image_{row_size}.tif')

print(f"done!")