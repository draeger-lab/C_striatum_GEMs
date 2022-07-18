# /models/

This folder contains all `**.xml` files coding for Genome Scale Metabolic Models. In this case we have four strain specific models and one model of the core metabolism for *Corynebacterium striatum*. 

The reconstructions are based on the following NCBI accessions. The Genome files were linked by BacDrive via DSMZ.

**Number** | **Name** | **DSM-number** | **NCBI accession** | **Other**
--- | --- | --- | --- | ---
14 | FDAARGOS\_1054 | [20668](https://www.dsmz.de/collection/catalogue/details/culture/DSM-20668) | [CP066290](https://www.ncbi.nlm.nih.gov/nuccore/CP066290.1/) | ATCC 6940
15 | FDAARGOS\_1197 | [45711](https://www.dsmz.de/collection/catalogue/details/culture/DSM-45711) | [CP069514](https://www.ncbi.nlm.nih.gov/nuccore/CP069514) | 
16 | FDAARGOS\_1115 | [7184](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7184) | [CP068158](https://www.ncbi.nlm.nih.gov/nuccore/CP068158) |  
17 | FDAARGOS\_1116 | [7185](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7185) | [CP068157](https://www.ncbi.nlm.nih.gov/nuccore/CP068157) | 

The `Cstr_core.xml` model was drafted by comparing the four strain specific models and only keeping common reactions and metabolites. It is not very developed at this point and rather conceptual then useful.
