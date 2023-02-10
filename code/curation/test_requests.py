#%%
import requests
import refinegems as rg
reac_url = 'http://bigg.ucsd.edu/api/v2/universal/reactions/'
metab_url = 'http://bigg.ucsd.edu/api/v2/universal/metabolites/'
#%%
mod = rg.load.load_model_cobra('../../models/Cstr_14.xml')
mod
#%%
requests.get(reac_url+'ADA').json().keys()
# %%
for metab in mod.metabolites:
    id = metab.id[:-2]
    print(id, requests.get(metab_url+id).json()['name'])
