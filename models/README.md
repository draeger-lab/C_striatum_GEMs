# /models/

This folder contains all `**.xml` files coding for Genome Scale Metabolic Models. In this case we have four strain specific models and one model of the core metabolism for *Corynebacterium striatum*. 

The reconstructions are based on the following NCBI accessions. The Genome files were linked by BacDrive via DSMZ and can be downloaded either from the NCBI or PATRIC.

**Number** | **Name** | **DSM-number** | **NCBI accession** | **Other**
--- | --- | --- | --- | ---
14 | FDAARGOS\_1054 | [20668](https://www.dsmz.de/collection/catalogue/details/culture/DSM-20668) | [CP066290](https://www.ncbi.nlm.nih.gov/nuccore/CP066290.1/) | ATCC 6940
15 | FDAARGOS\_1197 | [45711](https://www.dsmz.de/collection/catalogue/details/culture/DSM-45711) | [CP069514](https://www.ncbi.nlm.nih.gov/nuccore/CP069514) | 
16 | FDAARGOS\_1115 | [7184](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7184) | [CP068158](https://www.ncbi.nlm.nih.gov/nuccore/CP068158) |  
17 | FDAARGOS\_1116 | [7185](https://www.dsmz.de/collection/catalogue/details/culture/DSM-7185) | [CP068157](https://www.ncbi.nlm.nih.gov/nuccore/CP068157) | 

The `Cstr_core.xml` model was drafted by comparing the four strain specific models and only keeping common reactions and metabolites. It is not very developed at this point and rather conceptual then useful.

`Cstr_KC-Na-01.xml` was created by Tanja Urz in a research project and curated by Famke Bäuerle in a research project prior to this thesis. It provides information on the strain `KC-Na-01` which is not available for laboratory experiments but is the only strain present in the KEGG database. This model had no metabolites which were without charge. Duplicate reaction and metabolite removal still needs to be done, but the manual annotations as well as metabolite annotation synchronization has been done.

## Checklist for model FDAARGOS\_1054

_You can use the table shown in the README file from this repo as a way to track the MEMOTE score between the following steps. This checklist was developed by Alina Renz during her PhD thesis._

- [ ] 1. **Decide for an organism of interest.** Denote name and strain.
    - [ ] Check whether the strain is available on the DSMZ for laboratory use.
- [ ] 2. **Database search:** Search in different databases for already existing models of your organism.
    - [ ] [BioModels](https://www.ebi.ac.uk/biomodels/)
    - [ ] [Path2Models](https://www.ebi.ac.uk/biomodels/p2m/browse)
    - [ ] [BiGG](http://bigg.ucsd.edu/models)
    - [ ] [Virtual Metabolic Human](https://www.vmh.life/) - [its available](https://www.vmh.life/#microbe/Corynebacterium_striatum_ATCC_6940)
    - [ ] Other
#### Draft reconstruction
- [ ] 3. **Generate a first draft of your GEM with CarveMe.** Write down CarveMe, Diamond and CPLEX version in a table.
- [ ] 4. **Initial Analysis of the model**
    - [ ] Number of Reactions, Metabolites, Genes
    - [ ] SBML-Version
    - [ ] MEMOTE score
    - [ ] How many genes does the organism have?
    - [ ] How many genes code for hypothetical proteins?
    - [ ] How many genes are still missing in the model (excluding hypothetical)?
#### Add annotations
- [ ] 5. **Annotations:** Add annotations to the model. Either extract them from the ‘notes’ field (you can use refineGEMs for this) or use ModelPolisher. When you use the ModelPolisher, keep in mind to re-check all bounds, the objective function, and the genes! Write down the ModelPolisher version. 
    - [ ] Bounds
    - [ ] Objective function
    - [ ] Genes
- [ ] 6. **KEGG Gene annotations:** If your organism also occurs in the KEGG database, add the KEGG Gene ID (Locus tag) as gene annotations
- [ ] 7. SBO Terms: The Systems Biology Ontology (SBO) contains a set of controlled vocabularies that are commonly used in systems biology. Every item in our GEMs can be labeled with an SBO-Term, including all genes, metabolites, and reactions. SBO-terms can be added using libSBML. You can use refineGEMs for this, write down the used version.
    - [ ] Genes
    - [ ] Metabolites
    - [ ] Reactions
- [ ] 8. **Add ECO terms:** The Evidence and Conclusion Ontology (ECO) terms provide information about the curator's confidence about a reaction's inclusion into the model. The use of ECO terms is advised over the use of confidence scores, as confidence scores are not uniquely defined in the literature. ECO terms may be added based on the genes' evidence in a reaction's gene-protein-reaction association (GPR). If no GPR is associated with a reaction, the reaction obtains the ECO term with the lowest confidence score. Based on the evidence level of the genes in the GPR, ECO terms are added to the reactions. A helpful resource is the UniProt database, where the protein existence column gives information about the evidence level of a particular gene (inferred from homology, evidence at protein level, etc.).
- [ ] 9. **Add KEGG Pathways:** If your organism occurs in the KEGG database, extract the KEGG reaction ID from the annotations of your reactions and identify, in which KEGG pathways this reaction occurs. Add all KEGG pathways for a reaction then as annotations with the biological qualifier ‘OCCURS_IN’ to the respective reaction. You can use refineGEMs for this, write down the used version.
#### Corrections and Improvements
- [ ] 10. **Check the chemical formulas:** CarveMe adds the chemical formula of a metabolite to the ‘notes’-field. Transfer the chemical formula from the ‘notes’-field to the species description using the libSBML fbc-package. If you used the --fbc2 option during the model generation with CarveMe, check, whether the chemical formulas were correctly transferred from the ‘notes’-field.
- [ ] 11. **Check the charges:** Charges are missing in the description of the model’s metabolites. The BiGG database, however, can be used to identify the charge for a given metabolite.
Keep in mind that sometimes, more than one charge is given in the database.
- [ ] 12. **Correct Mass and Charge Imbalances:** Mass and charge imbalanced reactions can be reported by COBRApy and also memote returns a list of mass and charge imbalanced reactions in the report. Evaluate the mass and charge imbalanced reactions and try to fix them. You can use the MCC tool, write down the used version.
- [ ] 13. **Reduce Orphan and Dead-end metabolites:** Get a list of dead-end and orphan metabolites and try to identify reactions that can be added to connect the metabolites further to the network.
- [ ] 14. **Check for energy-generating cycles (EGC):** Models may contain thermodynamically infeasible energy-generating cycles. These models can produce energy without consuming nutrients. Fritzemeier et al. (DOI: 10.1371/journal.pcbi.1005494) suggested a pipeline to identify the 14 different energy metabolites ATP, CTP, GTP, UTP, ITP, NADH, NADPH, FAD, FADH, ubiquinol-8, menaquinol-8, 2-demethylmenaquinol 8, acetyl-CoA, and L-glutamate. Add a dissipation reaction for each metabolite, constrain all uptake rates to zero and subsequently maximize each dissipation reaction. If any optimization returns a result unequal zero, you have identified an energy-generating cycle that needs to be eliminated. You can use refineGEMs for this.
- [ ] 15. **Improve the biomass objective function (BOF):** As CaveMe provides a universal biomass equation, you can further improve and specify the BOF of your organism. One possibility is to use the Python package BOFdat (DOI: 10.1371/journal.pcbi.1006971). The stoichiometric coefficients for (i) major macromolecules, (ii) inorganic ions and coenzymes, and (iii) the remaining species-specific metabolic biomass precursors are calculated and incorporated into the BOF. If genomics, transcriptomics, proteomics, lipidomics, or other experimental data is available, you can use BOFdat to refine your organism's BOF.
#### Model extension
- [ ] 16. **Add further reactions:** If your organism also occurs in the KEGG database, search for genes that are so far not included in the model. Identify the reactions associated with those genes and add these reactions to the model. Keep track of the model properties: Number of Reactions, Metabolites, Genes and Memote Score.
#### Model validation
- [ ] 17. **Compare model predictions to experimental data:** To validate your GEM, search the literature for experimental results from your organism, or even strain, of interest. These results could include additional growth media (e.g., M9 or LB), auxotrophies, gene essentialities, or other physiological properties. Simulate the conditions described in the laboratory experiment and compare the in silico and in vitro results.
    - [ ] Do your *in silico* results agree with the *in vitro* results?
    - If your results do not agree with the experimental results, identify where the discrepancy comes from. Check whether you
    - [ ] need to add reactions to the model
    - [ ] need to eliminate reactions from the model
    - [ ] need to change the directionality of reactions
    - [ ] have identified a knowledge gap
- [ ] 18. **Growth on SNM3:** We are highly interested in organisms that grow in the human nose. In Tübingen, a medium that mimics the nasal environment was experimentally developed: the Synthetic Nasal Medium (SNM3) (https://doi.org/10.1371/journal.ppat.1003862). 
    - [ ] Use the defined medium to simulate the growth of your organism in the human nose. To do so, change the uptake rate (lower bound) of the respective metabolite to 10.0 mmolgDW-1 h- 1. Oxygen should get an uptake rate of 20.0 mmolgDW-1 h-1. All other exchange reactions for metabolites that are not listed as components of the SNM3 should have an uptake rate of 0 mmolgDW-1 h-1. You can use refineGEMs for this.
    - [ ] If your organism does not grow on SNM3, identify which additional compounds are required to enable growth. One approach is to compare the originally active exchange reactions to the exchange reactions that are defined by the SNM3.
    - [ ] If you have identified metabolites that are required for growth but not defined in SNM3, do some literature research to figure out whether the specific metabolite can internally be produced in your organism. If this is the case, add the missing reactions, metabolites, and genes to the model and test the growth on SNM3 again.
- [ ] 19. **Behavior with and without oxygen:** Check whether your organism is anerobic, aerobic or a facultative anaerobe. This should be reflected in the GEMs abilitz to grow with and without oxygen.
#### Model publication
- [ ] 20. **Make the model available:** Make your model available in a modeling database to meet the FAIR data principle (findable, accessible, interoperable, and reusable). Before uploading the model.
    - [ ] check one last time whether your model is a valid SBML file.
    - [ ] Additionally, check whether your model complies with the minimum standardized content for a metabolic network reconstruction (DOI: 10.15252/msb.20199235, Box 2).
    - [ ] Write down the final model properties
    - [ ] Upload the valid SBML file to, e.g., BioModels. You can use a COMBINE archive and the OMEX file format (DOI: 10.1186/s12859-014-0369-z) to share all information of your model, including, e.g., media definitions. For BioModels, you can gain reviewers' access there. Then, the model is initially only visible with the corresponding log-in credentials. After publishing your model in, e.g., a scientific journal, don't forget to make your model publicly available to everyone.