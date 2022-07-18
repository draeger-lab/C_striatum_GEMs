# /escher/

When the xml files in the `models` folder are updated, the corresponding `**.json` files are updated with the automatic github action `memote.yml`. 

The `**_FBA.csv` are updated when the github action `escher.yml` is triggered manually. They contain information on fluxes which can be visualized on escher maps.

The `**.json` files can be used to draw escher maps using either the local tool or the [web-tool](https://escher.github.io/#/).

- `/egc/` contains maps drawn with reactions that had fluxes while looking for EGCs.
- `/maps/` contains generic maps that were updated with the specific *C. striatum* models to look for missing reactions.
-`pathways` contains metabolism maps that were created with escher, using the `Cstr_14.json`. As "ground-truth" the [metabolic maps from KEGG](https://www.kegg.jp/brite/query=00561&htext=br08901.keg&option=-a&node_proc=br08901_org&proc_enabled=map&panel=collapse) were used.