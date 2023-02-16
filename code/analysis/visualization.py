
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

models = ['../models/Cstr_TS.xml','../models/Cstr_1197.xml','../models/Cstr_1115.xml','../models/Cstr_1116.xml','../models/Cstr_KC-Na-01.xml']
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
    create_venn(mods, 'm', True)
    plt.tight_layout()
    plt.show()
    #plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')

    name = 'reac'
    create_venn(mods, 'r', True)
    plt.tight_layout()
    plt.show()
    #plt.savefig('../analysis/comparison/' + name + '.png',bbox_inches='tight')
    
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

#%%
numbers.loc[3,:] = ['Memote score', 86.40, 86.65, 86.20, 86.56, 84.14]
numbers
#%%
#%%
with plt.rc_context({"axes.spines.right" : True}):
    ax = numbers.set_index(0).T.plot.bar(y=['metabolites', 'reactions', 'genes'], figsize=(8, 5), cmap='Paired')
    numbers.set_index(0).T.plot(y='Memote score', ax=ax, use_index=False, linestyle=':', secondary_y='Memote score', color='k', marker='D', legend=True)
    ax.right_ax.set_ylabel('Memote score [%]')
    ax.right_ax.legend(loc='upper right', bbox_to_anchor=[0.98, 0.9])
    ax.legend(title=False, loc='upper left', ncol=3)
    ax.right_ax.set_ylim([75, 95])
    ax.set_ylim([0,2500])
    ax.tick_params(axis='x',which='both', bottom=False,top=False)
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
conf = pd.read_excel('/Users/baeuerle/Organisation/Masterarbeit/Nextcloud/master_thesis/paper/Cstr V4/results_V4.xlsx', sheet_name='in silico').replace({'yes':1,'no':0})#.set_index('base')
s = conf[conf['data'] == 'growth on plain medium '].set_index('base').drop('data', axis=1)
conf = pd.read_excel('/Users/baeuerle/Organisation/Masterarbeit/Nextcloud/master_thesis/paper/Cstr V4/results_V4.xlsx', sheet_name='in vitro').replace({'yes':1,'no':0})#.set_index('base')
v = conf[conf['data'] == '24h-OD-fold-change > 2'].set_index('base').drop('data', axis=1)
# %%
con = pd.DataFrame(v == s)
#plt.figure(figsize=(10,8))
sns.heatmap(con, 
            cmap='RdYlBu', 
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

#%%
conf = pd.read_excel('/Users/baeuerle/Organisation/Masterarbeit/Nextcloud/master_thesis/paper/Cstr V4/results_V4.xlsx', sheet_name='in silico').replace({'yes':1,'no':0})#.set_index('base')
si = conf[conf['data'] == 'dt [min] (+missing)'].set_index('base').drop('data', axis=1)
si
# %%
conf = pd.read_excel('/Users/baeuerle/Organisation/Masterarbeit/Nextcloud/master_thesis/paper/Cstr V4/results_V4.xlsx', sheet_name='in vitro').replace({'yes':1,'no':0})#.set_index('base')
vi = conf[conf['data'] == 'dt [min] '].set_index('base').drop('data', axis=1)
vi
# %%
perc = {}
for medium in ['LB', 'RPMI']:
    perc[medium] = (vi[vi.index == medium]/si[si.index == medium])*100 - 100

df = pd.concat(perc, axis=0)
df.index.names = None, None
df = df.reset_index().drop('level_1',axis=1).set_index('level_0')
df.index.name = None
df
# %%
sns.heatmap(df.astype("float"), 
            cmap='RdYlBu', 
            linewidth=.5, 
            vmin = -150,
            vmax = 150,
            #center = 0.0,
            annot=True,
            fmt='.0f',
            cbar_kws = {'label':'dt difference [%]','orientation':'horizontal'}
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
plt.savefig('../analysis/comparison/heatmap_dt_comparison.png')
# %%
mods[0]
# %%
for rea in mods[0].metabolites.get_by_id('ncam_c').reactions:
    print(rea)
# %%
mods[0].reactions.get_by_id('NNDPR')
# %% SBO terms for bar chart
sbo_mapping={'658': 'passive transport', 
            '176': 'biochemical reaction', 
            '167': 'biochemical or transport reaction',
            '402': 'transfer of a chemical group', 
            '659': 'symporter-mediated transport', 
            '200': 'redox reaction', 
            '233': 'hydroxylation',
            '399': 'decarboxylation', 
            '178': 'cleavage', 
            '403': 'transamination', 
            '215': 'acetylation', 
            '377': 'isomerisation', 
            '657': 'active transport', 
            '216': 'phosphorylation', 
            '401': 'deamination', 
            '376': 'hydrolysis', 
            '217': 'glycosylation', 
            '660': 'antiporter-mediated transport', 
            '654': 'co-transport reaction', 
            '214': 'methylation', 
            '655': 'transport reaction', 
            '627': 'exchange reaction', 
            '632': 'sink reaction', 
            '629': 'biomass production',
            '630': 'ATP maintenance'}
print(len(sbo_mapping))
# %%
model = rg.load.load_model_libsbml(models[1])
#%%
sbos_dict = {}
for react in model.getListOfReactions():
    sbo = react.getSBOTerm()
    if sbo in sbos_dict.keys():
        sbos_dict[sbo] += 1
    else: 
        sbos_dict[sbo] = 1
print(sbos_dict)
print(len(sbos_dict))
# %%
for key in sbos_dict.keys():
    if str(key) not in sbo_mapping.keys():
        print(key)
# %%
sbos_names = {}
for key in sbos_dict.keys():
    sbos_names[sbo_mapping[str(key)]] = sbos_dict[key]
print(sbos_names)
#%%
sorted_sbos = {k: v for k, v in sorted(sbos_names.items(), key=lambda item: item[1])}
print(sorted_sbos)
# %%
labels = list(sorted_sbos.keys())
plt.figure(figsize=(10,8))

plt.xscale('log')
plt.barh(np.arange(len(sorted_sbos)), sorted_sbos.values(), height=.8, tick_label=labels)

# %%
sbo_maps = {}
for mod in models:
    model = rg.load.load_model_libsbml(mod)
    sbos_dict = {}
    for react in model.getListOfReactions():
        sbo = react.getSBOTerm()
        if sbo in sbos_dict.keys():
            sbos_dict[sbo] += 1
        else: 
            sbos_dict[sbo] = 1
    #print(sbos_dict)
    #print(len(sbos_dict))

    for key in sbos_dict.keys():
        if str(key) not in sbo_mapping.keys():
            print(key)

    sbos_names = {}
    for key in sbos_dict.keys():
        sbos_names[sbo_mapping[str(key)]] = sbos_dict[key]
    #print(sbos_names)

    sorted_sbos = {k: v for k, v in sorted(sbos_names.items(), key=lambda item: item[1])}
    #print(sorted_sbos)
    sbo_maps[model.getId()] = sorted_sbos
 #%%   
df = pd.DataFrame.from_dict(sbo_maps)#.plot.barh()
df = df[df['fda_1054'] > 3]
df = df.rename(STRAINS, axis=1)
df.plot.barh(width=.8, figsize=(8,10), color=cb, stacked=True)
#plt.xscale('log')
plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    left=False,
    )
# %%
