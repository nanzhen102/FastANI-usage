# FastANI usage
 The most practical protocol to calculate ANI values | Aspen (Nanzhen) Qiao | Dr. Michael Gänzle’s lab | 20250313

#### ANI (average nucleotide identity)

An ANI value of 95% (94–96%) has been almost consistently used in recent years to describe new bacterial species.

#### The final figure you will get 👉
[figure]

Ref: https://doi.org/10.1128/aem.01034-23




## Protocol 🧑‍🔧
#### Step 1. Prepare the genomes you will calculate.

Better format them as .fna files.


Make sure the number of genomes is correct.

```bash
ls -l | grep "^-" | wc -l
```

#### Step 2. Generate the genome list.

```bash
ls | grep ".fna$" > list.txt
```

#### Step 3. Run FastANI.

If you need to install FastANI:

```bash
conda create --name fastANI
conda activate fastANI
conda install bioconda::fastani

#if conda is not wroking, try mamba
mamba install fastANI
```

```bash
# check if fastANI is working
fastANI -h
fastANI --ql list.txt --rl list.txt -t 4 -o all_all_fastani_output.txt
# -t, threads
# --ql, query_list
# --rl, reference_list
# -o, output_file
```

#### Step 4. Turn the output file into a matrix.

Need two files here: `list.txt` & `all_all_fastani_output.txt`.

Run `fastani_output_to_matrix.py`(a Python script), and the matrix will be outputted as `fastani_matrix.csv`.

```python
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
```

#### Step 5. Integrate the matrix into the phylogenetic tree on iTOL.

- Log into iTOL (https://itol.embl.de/itol.cgi) and make sure the phylogenetic tree is ready.
- Download the spreadsheet to edit big phylogenetic trees easily (https://itoleditor.letunic.com/download/iTOL_annotation_editor_v1_8_Excel.xlsm).
- Log in → select the tree you are working on → create a new dataset → choose Heatmap → Label the dataset and pick up a legend color → paste the data.
- If needed, sort the data on the iTOL website.

#### Step 6. 🎉 🎈

🎉

