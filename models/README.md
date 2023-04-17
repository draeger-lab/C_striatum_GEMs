# /models/

This folder contains all `**.xml` files coding for Genome Scale Metabolic Models. In this case we have four strain specific models and one model of the core metabolism for *Corynebacterium striatum*. 

The reconstructions are based on the following NCBI accessions. The Genome files were linked by BacDrive via DSMZ and can be downloaded either from the NCBI or PATRIC.

**Short** | **Name** | **DSM-number** | **NCBI accession** | **Other**
--- | --- | --- | --- | ---
TS | FDAARGOS\_1054 | [20668](https://www.dsmz.de/collection/catalogue/details/culture/DSM-20668) | [GCA_016403285.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_016403285.1) | ATCC 6940, 14 (lab)
1197 | FDAARGOS\_1197 | [45711](https://www.dsmz.de/collection/catalogue/details/culture/DSM-45711) | [GCA_016889445.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_016889445.1) | 15 (lab)
1115 | FDAARGOS\_1115 | [7184](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7184) | [GCA_016728105.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_016728105.1) | 16 (lab)
1116 | FDAARGOS\_1116 | [7185](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7185) | [GCA_016728205.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_016728205.1) | 17 (lab)
KC | iCstrKCNa01FB23 | | [GCA_002156805.1](https://www.ncbi.nlm.nih.gov/assembly/GCF_002156805.1)

The `Cstr_core.xml` model was drafted by comparing the four strain specific models and only keeping common reactions and metabolites. It is not very developed at this point and rather conceptual then useful.

`iCstrKCNa01FB23.xml` was created by Tanja Urz in a research project and curated by Famke Bäuerle in a research project prior to this thesis. It provides information on the strain `iCstrKCNa01FB23` which is not available for laboratory experiments but is the only strain present in the KEGG database. This model had no metabolites which were without charge. Duplicate reaction and metabolite removal still needs to be done, but the manual annotations as well as metabolite annotation synchronization has been done.