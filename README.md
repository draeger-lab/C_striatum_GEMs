[![Memote Report](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote.yml/badge.svg)](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# C_striatum_GEMs
This repository contains all changes made to the strain specific models of *Corynebacterium striatum*.

Note: creating the memote report written to `GEM_status.html` will take around 10 minutes. You will need to pull afterwards for the updated file.

To access older versions of the model and the corresponding report browse the commits and choose the corresponding commit.

Please link specific additions to the respective issues to track the work you did (#1: model changes, #2: analysis / simulation, #3: novel additions).

More information on what to expect in the different folder is given in separate READMEs located in the folders.
## Log of substantial changes to the models
**Model status** | **Tool / Code** | **Date** | **Commit tag**
--- | --- | --- | ---
Draft models | CarveMe v.1.5.1 | 25.08.2021 | Initial commit
Cleaned draft models | refinegems.polish_carveme | 28.03.2022 | v1.0
Polished draft models | ModelPolisher | 29.03.2022 | v2.0
Specified SBO Terms | refinegems.sbo_annotation | 03.04.2022 | v3.0
Corrected charges | refinegems.charges + scripts/man_cur_charges.py | 05.04.2022 | v4.0
Annotated GPRs and metabolites | refinegems.polish_carveme +  scripts/man_cur_annotate.py | 07.04.2022 | v5.0
Removed duplicate reactions | scripts/man_cur_dupreac.py | 21.04.2022 | v6.0
Redo manual steps in case something is missing | scripts/. | 22.04.2022 | v6.1
Added units to all parameters | refinegems.polish_carveme | 27.04.2022 | v6.2
Used MCC tool on all strains | scripts/man_cur_mcc.py | 01.07.2022 | v7.0
Removed SIRA2, FPRA and GCDH from all strains | scripts/man_cur_egc.py | 01.07.2022 | v7.1

## Tricks
Revert only model files:
1. search for commit hash in commit history
2. `git checkout [commit ID] -- path/to/file`
3. commit and push
