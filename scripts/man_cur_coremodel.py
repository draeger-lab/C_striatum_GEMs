#%%
import cobra
import pandas as pd
from refinegems import load_model_cobra
from cobra import Model, Reaction, Metabolite

models = ['../models/Cstr_14.xml', '../models/Cstr_15.xml',
          '../models/Cstr_16.xml', '../models/Cstr_17.xml']
mod_load = []
for mod in models:
    model = load_model_cobra(mod)
    mod_load.append(model)

#%%
rea = {}    
for mod in mod_load:
    reac = mod.reactions
    res = []
    for re in reac:
        res.append(re.id)
    rea[mod.id] = res

#%%
set(rea['fda_1054']).symmetric_difference(rea['fda_1197']) #558
set(rea['fda_1197']).symmetric_difference(rea['fda_1115']) #370
set(rea['fda_1197']).symmetric_difference(rea['fda_1116']) #444

common_rea = set(rea['fda_1054']).intersection(rea['fda_1116']).intersection(rea['fda_1115']).intersection(rea['fda_1197'])

#%%
core = Model('Cstr_core')
for reac in common_rea:
    reaction = mod_load[0].reactions.get_by_id(reac)
    core.add_reactions([reaction])

#%%
reaction = mod_load[0].reactions.get_by_id("Growth")
core.add_reactions([reaction])
core.reactions
#%%
core.objective = 'Growth'
core.optimize()
core.summary()
#%%
core.boundary
len(set(core.reactions) - set(core.boundary)) #1274
#%%
from cobra.io import write_sbml_model
write_sbml_model(core, '../models/Cstr_core.xml')