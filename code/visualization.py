
#%%# this is a script to automatically generate and update visualization of the models
from venn import venn, pseudovenn
import cobra
from libsbml import *
import refinegems as rg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PARAMS import *

#%%
models = ['../models/Cstr_14.xml','../models/Cstr_15.xml','../models/Cstr_16.xml','../models/Cstr_17.xml','../models/Cstr_KC-Na-01.xml']
mods = []
for mod in models:
    mods.append(rg.load.load_model_cobra(mod))

#%% Venn diagrams
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


# %% barcharts
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
# %% heatmap

growth = pd.read_csv('../analysis/growth_20230113_minimal_uptake.csv')[['model', 'medium', 'doubling_time [min]']]
growth=growth.set_index(['medium', 'model']).sort_index().T.stack()
growth.columns.name=None
growth.index.names = (None,None)
growth.index.name=None
growth.index = growth.index.get_level_values(1)
growth.replace([np.inf, -np.inf], np.nan, inplace=True)
growth
#%%
plt.figure(figsize=(10,8))
sns.heatmap(growth.T, 
            annot=True, 
            annot_kws={"fontsize":15},
            vmin=20, vmax=80,
            #cmap='crest', 
            linewidth=.5, 
            cbar_kws = {'orientation':'horizontal', 'label':'doubling time [min]'}
            )
plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    )
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,
    )
plt.savefig('../analysis/comparison/heatmap_dt.png')