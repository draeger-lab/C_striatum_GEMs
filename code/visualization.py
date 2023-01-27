
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

STRAINS = {'fda_1054':'TS', 
            'fda_1197':'1197',
            'fda_1115':'1115',
            'fda_1116':'1116',
            'KC_Na_01':'KC',
            }
STRAINS_LAB = {'14':'TS', 
            '15':'1197',
            '16':'1115',
            '17':'1116',
            }
MEDIA = {'CGXlab':'CGXII'}

models = ['../models/Cstr_14.xml','../models/Cstr_15.xml','../models/Cstr_16.xml','../models/Cstr_17.xml','../models/Cstr_KC-Na-01.xml']
#%%
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
        intersec[STRAINS[model.id]] = set(reas)
    if perc:
        fig = venn(intersec, fmt="{percentage:.0f}%")
    else:
        fig = venn(intersec)
    return fig

#%%
with plt.rc_context({'font.size': 75}):
    name = 'metabs'
    create_venn(mods, 'm', False)
    plt.tight_layout()
    plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')

    name = 'reac'
    create_venn(mods, 'r', False)
    plt.tight_layout()
    plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')
    
    name = 'metabs_14_16'
    create_venn([mods[0],mods[2]], 'm', False)
    plt.tight_layout()
    plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')

    name = 'reac_14_16'
    create_venn([mods[0],mods[2]], 'm', False)
    plt.tight_layout()
    plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')

plt.close('all')

# %% barcharts
numbers = pd.DataFrame(['reactions', 'metabolites', 'genes'])
numbers
#%%
for model in mods:
    numbers[STRAINS[model.id]] = [len(model.metabolites), 
                                  len(model.reactions), 
                                  len(model.genes)]
numbers
# %%
numbers.set_index(0).T.plot.bar(cmap='Paired')#color={'reactions': cb[2], 'metabolites': cb[1], 'genes': cb[0]})
plt.legend()
plt.xticks(rotation=0)
plt.yticks(np.asarray([0,500,1000,1500,2000, 2500]))
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    )
plt.tight_layout()
plt.savefig('../analysis/comparison/numbers.png')
# %% heatmap

growth = pd.read_csv('../analysis/growth_20230113_minimal_uptake.csv')[['model', 'medium', 'doubling_time [min]']]
growth=growth.set_index(['medium', 'model']).sort_index().T.stack()
growth.columns.name=None
growth.index.names = (None,None)
growth.index.name=None
growth.index = growth.index.get_level_values(1)
growth.replace([np.inf, -np.inf], np.nan, inplace=True)
growth.drop('SNM3', inplace=True, axis=1)
growth.rename(STRAINS, inplace=True)
growth.rename(MEDIA, axis=1, inplace=True)
growth = growth.T[['TS', '1197', '1115', '1116', 'KC']].T
growth
#%%
plt.figure(figsize=(10,8))
sns.heatmap(growth.T, 
            annot=True, 
            annot_kws={"fontsize":15},
            vmin=20, vmax=80,
            #cmap='crest', 
            linewidth=.5, 
            cbar_kws = {'orientation':'horizontal', 'label':'doubling time [min]'},
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

# %% bar chart for pathways

model = rg.load.load_model_libsbml(models[0])
model
#%%
groups = {}
for gr in model.getPlugin(1).getListOfGroups():
    groups[gr.getName()] = gr.getNumMembers()

sel = {}
other = 0
for name, value in groups.items():
    if value > 10 and name != 'Metabolic pathways':
        sel[name] = value
    else:
        other = other + value
#sel['Other Pathways'] = other
names = list(sel.keys())
values = list(sel.values())
plt.barh(range(len(sel)), values, tick_label=names)
# %%
#%%
from ols_client import EBIClient
c = EBIClient()

#%%
for a in c.get_ontologies():
    print(a
        )
#%%
for reac in model.getListOfReactions():
    print(reac.getSBOTermID())
    print(c.get_term('sbo','http://biomodels.net/SBO/SBO_0000' + str(reac.getSBOTerm())))
    
#%%
conf = pd.read_excel('/Users/baeuerle/Organisation/Masterarbeit/Nextcloud/master_thesis/paper/Cstr V4/results_V4.xlsx', sheet_name='confirmation').replace({'yes':1,'no':0})#.set_index('base')
conf
# %%
conf.T['new'] = 1
conf
v = conf[conf['data'] == '24h-OD-fold-change > 2'].drop('data', axis=1).set_index('base')
s = conf[conf['data'] == 'growth on plain medium '].drop('data', axis=1).set_index('base')
con = pd.DataFrame(v == s)
#plt.figure(figsize=(10,8))
sns.heatmap(con, 
            cmap='RdBu', 
            linewidth=.5, 
            cbar=False,
            )
plt.ylabel('')
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
plt.tight_layout()
plt.savefig('../analysis/comparison/heatmap_binary_comparison.png')