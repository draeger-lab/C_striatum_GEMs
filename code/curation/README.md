# Overview on manual curation scripts

Manual curation of the models which can be found in the `models` folder was done with a combination of scripts and manual adjustments to the models themselves. Manual adjustments were only done a few times, they are documented via the model version history.

* `wetlab_transfer`

Some of the manual curation scripts are now available from within the [refineGEMs](https://github.com/draeger-lab/refinegems) Python package. They are still a part of this repository for the sake of completeness. These are marked with DEPR_ for deprecated


The table below shows an overview on all scripts that were used during the curation part of the project. In parallel I developed the refineGEMs toolbox and used functions from refineGEMs as well.

**script** | **usage**  | **refinegems** | **author**
--- | --- | --- | ---
DEPR_manually_annotate | manual annotations inferred from `data/manual_curation.xlsx`| implemented 18.07.22 | FB
add_charges_from_P-putida | addition of manually researched charges and charges from the *P. putida* model | - | FB
man_cur_coremodel | drafting a core model from multiple strain specific models | possible | FB
man_cur_dupmetab | code for manual removal of duplicate metabolites identified manually or with memote | possible, store list in excel? | FB
man_cur_dupreac | code for manual removal of duplicate reactions identified manually or with memote | possible, store list in excel? | FB
man_cur_egc | investigation of Energy Generating Cycles | halfway implemented, needs testing and docs (18.07.22) | FB
man_cur_growth | manual investigation of growth behaviour, slightly inconclusive (18.07.22) | - | FB
man_cur_mcc | application of the MCC tool to all models | - | "Finn Mier"
man_cur_params | set params and look for flux bound | possible, with polish_carveme? | FB