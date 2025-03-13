import pandas as pd
import numpy as np

list_file = './list.txt'
fastani_file = './all_all_fastani_output.txt'
output_matrix_file = './fastani_matrix.csv'

# Load genome list
def load_genomes(list_file):
    with open(list_file, 'r') as f:
        genomes = [line.strip() for line in f]
    return genomes

# Load FastANI data and construct matrix
def construct_matrix(fastani_file, genomes):
    genome_index = {genome: i for i, genome in enumerate(genomes)}
    matrix_size = len(genomes)
    fastani_matrix = np.full((matrix_size, matrix_size), np.nan)  # Initialize with NaN

    with open(fastani_file, 'r') as f:
        for line in f:
            cols = line.strip().split('\t')
            if len(cols) < 3:
                continue
            g1, g2, ani_value = cols[0], cols[1], float(cols[2])
            if g1 in genome_index and g2 in genome_index:
                i, j = genome_index[g1], genome_index[g2]
                fastani_matrix[i, j] = ani_value
                fastani_matrix[j, i] = ani_value  # Ensure symmetry

    # Fill diagonal with 100.0 (self-comparison)
    np.fill_diagonal(fastani_matrix, 100.0)
    return pd.DataFrame(fastani_matrix, index=genomes, columns=genomes)

# Save matrix for Excel (CSV format)
def save_matrix(matrix, output_file):
    matrix.to_csv(output_file, sep=',')

if __name__ == '__main__':
    genomes = load_genomes(list_file)
    fastani_matrix = construct_matrix(fastani_file, genomes)
    save_matrix(fastani_matrix, output_matrix_file)
    print(f"FastANI matrix saved to {output_matrix_file}")
