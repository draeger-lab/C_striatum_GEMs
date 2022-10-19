# /code/

This folder contains manual curation scripts that were used to investigate and / or manipulate the models denoted in the `models` folder.

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
simulate_growth_single | carbon, nitrogen, phosophorous and sulfur sources | possible | Hawkey et al., 2022