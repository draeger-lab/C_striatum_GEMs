# /code/

This folder contains scripts that were used to investigate or manipulate the models denoted in the `models` folder.

The table below shows an overview on all notebooks and scripts that were used to investigate the models and get information about their growth behavior on different media.

**name** | **type** | **usage** | **author**
--- | --- | --- | ---
additives | notebook
M9 | notebook
media | notebook
simulate_growth_single | script | carbon, nitrogen, phosophorous and sulfur sources | Hawkey et al., 2022
single_gene_knockouts | script | gene knockouts | Hawkey et al., 2022
visualization | script
wetlab_transfer | notebook

The table below shows an overview on all scripts that were used during the curation part of the project. In parallel I developed the refineGEMs toolbox and used functions from refineGEMs as well.

**script** | **usage**  | **refinegems** | **author**
--- | --- | --- | ---
man_cur_annotate | manual annotations inferred from `data/manual_curation.xlsx`| implemented 18.07.22 | FB
man_cur_charges | addition of manually researched charges and charges from the *P. putida* model | - | FB
man_cur_coremodel | drafting a core model from multiple strain specific models | possible | FB
man_cur_dupmetab | code for manual removal of duplicate metabolites identified manually or with memote | possible, store list in excel? | FB
man_cur_dupreac | code for manual removal of duplicate reactions identified manually or with memote | possible, store list in excel? | FB
man_cur_egc | investigation of Energy Generating Cycles | halfway implemented, needs testing and docs (18.07.22) | FB
man_cur_growth | manual investigation of growth behaviour, slightly inconclusive (18.07.22) | - | FB
man_cur_mcc | application of the MCC tool to all models | - | "Finn Mier"
man_cur_params | set params and look for flux bound | possible, with polish_carveme? | FB