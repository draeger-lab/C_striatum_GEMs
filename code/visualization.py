
#%%# this is a script to automatically generate and update visualization of the models
from venn import venn, pseudovenn
import cobra
from libsbml import *
import refinegems as rg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PARAMS import *

#%%
models = ['../models/Cstr_14.xml','../models/Cstr_15.xml','../models/Cstr_16.xml','../models/Cstr_17.xml','../models/Cstr_KC-Na-01.xml']
mods = []
for mod in models:
    mods.append(rg.load.load_model_cobra(mod))

#%%
def create_venn(mods, entity, perc=False): 
    intersec = {}
    for model in mods:
        reas = []
        if entity == 'm':
            for rea in model.metabolites:
                reas.append(rea.id)
        if entity == 'r':
            for rea in model.reactions:
                reas.append(rea.id)
        intersec[model.id] = set(reas)
    if perc:
        fig = venn(intersec, fmt="{percentage:.0f}%")
    else:
        fig = venn(intersec)
    return fig


name = 'metabs'
create_venn(mods, 'm', False)
plt.tight_layout()
plt.savefig('../analysis/comparison/' + name + '.png')

name = 'reac'
create_venn(mods, 'r', False)
plt.tight_layout()
plt.savefig('../analysis/comparison/' + name + '.png')


# %%
numbers = pd.DataFrame(['reactions', 'metabolites', 'genes'])
numbers
#%%
for model in mods:
    numbers[model.id] = [len(model.metabolites), len(model.reactions), len(model.genes)]
numbers
# %%
numbers.set_index(0).T.plot.bar(cmap='Paired')#color={'reactions': cb[2], 'metabolites': cb[1], 'genes': cb[0]})
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.yticks(np.asarray([0,500,1000,1500,2000, 2500]))
# %%
