[![Memote Report](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote.yml/badge.svg)](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# C_striatum_GEMs
This repository contains all changes made to the strain specific models of *Corynebacterium striatum*.

Note: creating the memote report written to `GEM_status.html` will take around 10 minutes. You will need to pull afterwards for the updated file.

To access older versions of the model and the corresponding report browse the commits and choose the corresponding commit.

Please link specific additions to the respective issues to track the work you did (#1: model changes, #2: analysis / simulation, #3: novel additions).

More information on what to expect in the different folder is given in separate READMEs located in the folders.

## *Corynebacterium striatum*
<img align="right" src="./data/Cstr_16_TSB.png" height="200"
title="Colony morphology <i>C. striatum</i>"
style="display: inline-block; margin: 0 auto; max-width: 300px"/>
*Corynebacterium striatum*, a gram-positive and non-sporulating rod, has recently been discovered for its pathogenic properties. Even though it has been known since the early 20th century, C.striatum was often disregarded as a pathogen since it is part of the typical human skin microbiota<sup>[1](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5655097/)</sup>. Nevertheless, it was found that, especially in immunocompromised patients, C.striatum can be the source for diseases such as Chronic Obstructive Pulmonary Disease, also known as COPD or pneumonia<sup>[2](https://jidc.org/index.php/journal/article/view/31954008)</sup>. Not only is *C. striatum* active within the respiratory tract, but it was also attributed to long-standing open wound infections<sup>[3](http://europepmc.org/article/MED/28208859)</sup> and prolonged hospitalizations<sup>[4](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6037610/)</sup>.

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

## Software 
**Name** | **Version** | **More Information**
--- | --- | --- 
diamond | 2.0.11 | [github wiki](https://github.com/bbuchfink/diamond/wiki)
CPLEX | 20.1.0 | [product website](https://www.ibm.com/de-de/products/ilog-cplex-optimization-studio)
CarveMe | 1.5.1 | [docs](https://carveme.readthedocs.io/en/latest/)
libSBML | 5.19.0 | [github](https://github.com/sbmlteam/libsbml)
COBRApy | 0.25.0 | [docs](https://cobrapy.readthedocs.io/en/latest/)
refineGEMs | 0.0.1 | [repository](https://github.com/draeger-lab/refinegems)
