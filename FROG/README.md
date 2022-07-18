# /FROG/

Contains FROG analysis of all models in the `models` folder. The analysis will take place when the github action `frog.yml` is triggered manually. 

The FROG references are central to assessing the reproducibility of the model and the curation efforts.

The analysis is carried out using the [fbc_curation](https://github.com/matthiaskoenig/fbc_curation) tool.

FROG stands for 
1. **O**bjective Function Values

The objective function value for a defined set of bounds should be comparable/reproducible.
2. **F**lux Variability Analysis (FVA)

FVA span: min/max of flux should be comparable (for a particular objective function value). These values will have only small numerical differences among software, depending on the set boundary conditions.
3. **G**ene Deletion Fluxes

The systematic deletion of all genes one at a time should provide comparable reference results.
4. **R**eaction Deletion (extended coverage of reaction network)

The systematic deletion of all reactions one at a time should provide comparable reference results.

Source: [FROG analysis - a community standard to foster reproducibility and curation of constraint-based models](https://www.ebi.ac.uk/biomodels/curation/fbc)
