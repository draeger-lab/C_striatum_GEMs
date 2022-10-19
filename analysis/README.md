# /analysis/

This folder contains analysis files of the models which can be found in the `models` folder.

- `/hawkey/` contains carbon, nitrogen, phosphor and sulfur source report generated with scripts from [Hawkey et al., 2022](https://genome.cshlp.org/content/32/5/1004.full)
- `/mcc/` contains reports generated from the [MassChargeCuration](https://github.com/Finnem/MassChargeCuration) package.
- `/minimal_media/` contains tables created with the cobrapy minimal_medium function. Since this runs for a bit it makes sense to save th eoutput from time to time.
- The `/stats_**/` folders contain reports from the [refinegems](https://github.com/draeger-lab/refinegems) package, concerning number of entities and growth behaviour.
- `growth_<date>.xlsx` was also generated with [refinegems](https://github.com/draeger-lab/refinegems) and gives an overview growth comparison of all models.