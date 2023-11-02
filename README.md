[![Memote Report](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote_and_json_conversion.yml/badge.svg)](https://github.com/draeger-lab/C_striatum_GEMs/actions/workflows/memote_and_json_conversion.yml) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![standard-GEM](https://img.shields.io/badge/standard--GEM-yes-success)](https://github.com/MetabolicAtlas/standard-GEM)
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

## How to cite
Famke Bäuerle, Gwendolyn O. Döbel, Laura Camus, Simon Heilbronner, and Andreas Dräger. 
Genome-scale metabolic models consistently predict *in vitro* characteristics of *Corynebacterium
striatum*. Front. Bioinform., oct 2023. [doi:10.3389/fbinf.2023.1214074](https://doi.org/10.3389/fbinf.2023.1214074).

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
refineGEMs | 0.0.1 | [repository](https://github.com/draeger-lab/refineGEMs)
MassChargeCuration | 0.1 | [repository](https://github.com/Biomathsys/MassChargeCuration)
ModelPolisher | 2.0.1 | [repository](https://github.com/draeger-lab/ModelPolisher)
