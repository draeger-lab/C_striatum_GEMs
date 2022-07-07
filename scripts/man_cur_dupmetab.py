#%%
import cobra
from refinegems import load_model_cobra
model = load_model_cobra('../models/Cstr_14.xml')

#%%
cgly = list(model.metabolites.get_by_id('cgly_c').reactions)
glycys = list(model.metabolites.get_by_id('gly_cys__L_c').reactions)

for rea in cgly:
    print(rea)

print('---')
for rea in glycys:
    print(rea)
# %%
print(cgly[0]) #has more references
print(glycys[1])

#%%
print(cgly[2]) #has more references
print(glycys[0])

#%%
cgly = list(model.metabolites.get_by_id('cgly_e').reactions)
glycys = list(model.metabolites.get_by_id('gly_cys__L_e').reactions)

for rea in cgly:
    print(rea)

print('---')
for rea in glycys:
    print(rea)
    
#%%
from cobra.io import write_sbml_model
modelpaths_to_change = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']
for mod in modelpaths_to_change:
    model = load_model_cobra(mod)
    print(model.metabolites.get_by_id('cgly_c'))
    print(model.metabolites.get_by_id('cgly_e'))
    model.metabolites.get_by_id('gly_cys__L_c').remove_from_model()
    model.metabolites.get_by_id('gly_cys__L_e').remove_from_model()
    write_sbml_model(model, mod)