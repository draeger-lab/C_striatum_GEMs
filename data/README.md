# /data/

This folder contains all external data used in the curation of the models which can be found in the `models` folder.

- `genomes/.` holds all `.fasta` and `.gff` files of the strains
- `energy_dissipation_rxns.csv` contains reaction definitions used to find so called Energy-Generating-Cycles (EGC)
- `iJN1463.xml` is a model of *Pseudomonas putida* which was used to add charges to metabolites which had no denoted charges
- `manual_curation.xlsx` is a table with annotations for metabolites (sheet metabs) and missing reactions that were added to the models to fill gaps (sheet gapfill)