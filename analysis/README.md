# /analysis/

This folder contains analysis files of the models which can be found in the `models` folder.

- `/additives/` contains csv files with possible growth enhancing additives
- `/CGXII_base_medium/` contains base definitions for all strains of the CGXII medium with respect to which metabolites are needed to ensure growth
- `/comparison/` holds images created with the `code/analysis/visualization.py` script
- `growth_sim_comp/growth_<date>.xlsx/.csv` were generated with [refineGEMs](https://github.com/draeger-lab/refineGEMs) and give overview on growth comparison of all models.
- `/hawkey/` contains carbon, nitrogen, phosphor and sulfur source report generated with scripts from [Hawkey et al., 2022](https://genome.cshlp.org/content/32/5/1004.full)
- `/mcc/` contains reports generated from the [MassChargeCuration](https://github.com/Finnem/MassChargeCuration) package.
- `/minimal_media/` contains tables created with the cobrapy minimal_medium function. Since this runs for a bit it makes sense to save th eoutput from time to time.
- The `/stats_**/` folders contain reports from the [refineGEMs](https://github.com/draeger-lab/refineGEMs) package, concerning number of entities and growth behaviour.
- `/visualization/` holds images that visualize model properties and model overlaps created with [refineGEMs](https://github.com/draeger-lab/refineGEMs)
- `/VMH/` contains all information about the VMH model of the type strain ATCC 6940 / FDAARGOS_1054
- `GEM_status_afterdraft.html` is a MEMOTE diff report of the models after drafting with CarveME
