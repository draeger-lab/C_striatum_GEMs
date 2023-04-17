# Overview on manual curation scripts

Manual curation of the models which can be found in the `models` folder was done with a combination of scripts and manual adjustments to the models themselves. Manual adjustments were only done a few times, they are documented via the model version history. Model changes which need a bit more documentation were done within jupyter notebooks (`.ipynb`).

Some of the manual curation scripts are now available from within the [refineGEMs](https://github.com/draeger-lab/refineGEMs) Python package. They are still a part of this repository for the sake of completeness. These are marked with DEPR_ for deprecated

The table below shows an overview on all scripts that were used during the curation part of the project. In parallel I developed the refineGEMs toolbox and used functions from refineGEMs as well.

**file** | **usage**  | **availability** | **author**
--- | --- | --- | ---
apply_mcc.ipynb | application of the MCC tool to all models | . | "Finn Mier"
generate_coremodel.py | drafting a core model from multiple strain specific models | . | FB
remove_duplicate_metabolites.ipynb | code for manual removal of duplicate metabolites identified manually or with memote | . | FB
remove_duplicate_reactions.ipynb| code for manual removal of duplicate reactions identified manually or with memote | . | FB
remove_keggPathwayCVTerms_KC.py | takes model iCstrKCNa01FB23 and removes URIs for kegg.pathways since they were added incorrectly | . | FB
wetlab_transfer.ipynb | change models based on [wetlab experiments](https://github.com/draeger-lab/C_striatum_wetlab) | . | FB
DEPR_add_charges.ipynb | addition of manually researched charges and charges from the *P. putida* model | [MCC tool](https://github.com/Biomathsys/MassChargeCuration) | FB
DEPR_check_egc.py | investigation of Energy Generating Cycles | refineGEMs.investigate.get_egc | FB
DEPR_manually_annotate.py | manual annotations inferred from `data/manual_curation.xlsx`| refineGEMs.curate | FB
DEPR_polish_params.py | set params and look for flux bound | refineGEMs.polish | FB


## Fix duplicate genes

While using rg.polish, we realized that the gene for the type I pantothenate kinase was present twice in all models but with two distinct IDs. The respective genes are listed below and were replaced accordingly and the duplicates were removed.

* Strain TS: G_WP_086891689 -> G_lcl_CP066290_1_prot_QQE53208_1_131
* Strain 1197: G_WP_086891689 -> G_lcl_CP069514_1_prot_QRP18489_1_2222
* Strain 1115: G_WP_086891689 -> G_lcl_CP068158_1_prot_QQU77405_1_429
* Strain 1116: G_WP_086891689 -> G_lcl_CP068157_1_prot_QQU80022_1_600
* Strain KC: G_WP_086891689_1 only present in this form thus not removed