#%%
import cobra
#from sklearn.model_selection import RandomizedSearchCV
from refinegems import load_model_cobra
model = load_model_cobra('../models/Cstr_TS.xml')
#%%
cobra.medium.minimal_medium(model).index


dafault_uptake = ['EX_amp_e', 'EX_arg__L_e', 'EX_ca2_e', 'EX_cl_e', 'EX_cobalt2_e',
       'EX_cu2_e', 'EX_dcyt_e', 'EX_fe3_e', 'EX_fol_e', 'EX_gly_asn__L_e',
       'EX_glyc3p_e', 'EX_glyglygln_e', 'EX_hishis_e', 'EX_istfrnA_e',
       'EX_k_e', 'EX_malthp_e', 'EX_mg2_e', 'EX_mn2_e', 'EX_o2_e', 'EX_so4_e',
       'EX_tet_e', 'EX_thm_e', 'EX_udcpp_e', 'EX_ura_e', 'EX_zn2_e']

def simulate_carbon_sources(model, default_uptake):
    carbon_sources = ["EX_gly_e", 
                      "EX_fum_e", 
                      "EX_male_e", 
                      "EX_pyr_e", 
                      "EX_succ_e", 
                      "EX_glc__D_e", 
                      "EX_urea_e", 
                      "EX_22bipy_e",
                      "EX_boricacid_e", 
                      "EX_adocbl_e", 
                      "EX_4abz_e", 
                      "EX_pnto__R_e", 
                      "EX_pydam_e", 
                      "EX_nac_e",
                      'EX_fru_e',
                      'EX_succ_e',
                      'EX_gam_e',
                      'EX_glyald_e']
    nitrogen_source = ["EX_ala__L_e", "EX_arg__L_e", "EX_cys__L_e", "EX_glu__L_e", "EX_his__L_e", "EX_leu__L_e", "EX_lys__L_e", 
"EX_orn_e", "EX_phe__L_e", "EX_pro__L_e", "EX_ser__L_e", "EX_thr__L_e", "EX_trp__L_e", "EX_val__L_e", "EX_cit_e", "EX_btn_e",
"EX_ribflv_e", "EX_thm_e"]
    simulate = {}
    with model:
        model.medium = {i: 10.0 for i in default_uptake}
        print(model.medium)
        simulate['default uptake'] = model.optimize().objective_value
        remove = []
        #model.reactions.get_by_id('EX_o2_e').lower_bound = 0.
        # does not grow without oxygen
        carbon_sources.extend(nitrogen_source)
        for source in carbon_sources:
            try:
                model.reactions.get_by_id(source).lower_bound = 0.
            except (KeyError):
                print(source + ' not in model')
                remove.append(source)
        print(model.medium)
        carbon_sources = [x for x in carbon_sources if x not in remove]
        simulate['no carbon'] = model.optimize().objective_value
        for source in carbon_sources:
            model.reactions.get_by_id(source).lower_bound = -10.
            solution = model.optimize().objective_value
            simulate[source] = solution#(np.log(2) / solution) * 60
            model.reactions.get_by_id(source).lower_bound = 0.
            
    return simulate

simulate_carbon_sources(model, dafault_uptake)

#%%
ess = []
for reaction in model.reactions:
    with model as model:
        reaction.knock_out()
        model.optimize()
        if model.objective.value <= 11:
            print('%s blocked (bounds: %s), new growth rate %f $' %
                  (reaction.id, str(reaction.bounds), model.objective.value))
            ess.append(reaction.id)
            
ess
#%%
len(model.exchanges) # =233
len(model.medium) # =233
model.slim_optimize() # = 52.7
medium = model.medium
#print(medium["EX_o2_e"]) # KeyError: Default medium has no oxygen?!
medium["EX_o2_e"] = 0.0
{i:10.0 for i in medium}
model.medium = {i:10.0 for i in medium} # growth = 11.28 :)
model.slim_optimize()

#%%
from cobra.medium import minimal_medium
minimal_medium(model, 0.1, minimize_components=True)
#%%
min_medium = {'EX_ca2_e': 0.000521,
'EX_cl_e':             0.000521,
'EX_cobalt2_e':        0.000010,
'EX_cu2_e':         0.000071,
'EX_gly_cys__L_e':     3.929106,
'EX_istfrnB_e':     0.001452,
'EX_k_e':       0.019519,
'EX_mg2_e':        0.000868,
'EX_mn2_e':            0.000069,
'EX_o2_e':            10.000000,
'EX_pi_e':             0.098609,
'EX_so4_e':            0.000434,
'EX_zn2_e':            0.000034}
min_medium

import numpy as np
with model:
    model.medium = min_medium
    growth = model.slim_optimize() # = 0.099
    time = (np.log(2) / growth) * 60
time # 417

for key, value in min_medium.items():
    min_medium[key] = 10.0

with model:
    model.medium = min_medium
    growth = model.optimize() # = 0.099
    time = (np.log(2) / growth.objective_value) * 60
time # 390

#%%
min2 = minimal_medium(model, 0.8, minimize_components=4, open_exchanges=True)
#%%
min2.to_csv('../analysis/growth/Cstr_14_minmed.csv')
#%%
aerob1 = min2[1].loc[min2[1] > 0] #aerob
aerob2 = min2[2].loc[min2[2] > 0] #aerob
min2[0].loc[min2[0] > 0] #anaerob
min2[3].loc[min2[3] > 0] #anaerob
#%%

a1_only = aerob1.reset_index()[~aerob1.reset_index()['index'].isin(aerob2.reset_index()['index'])].dropna()
a1_only = list(a1_only['index'])
['EX_chols_e', 'EX_ile__L_e', 'EX_istfrnA_e']
#%%
a2_only = aerob2.reset_index()[~aerob2.reset_index()['index'].isin(aerob1.reset_index()['index'])].dropna()
a2_only = list(a2_only['index'])
['EX_ala_L_Thr__L_e', 'EX_salchs4fe_e', 'EX_so4_e']
#%%
common = aerob2.reset_index()[aerob2.reset_index()['index'].isin(aerob1.reset_index()['index'])].dropna()
common=list(common['index'])
['EX_ca2_e',
 'EX_cl_e',
 'EX_cobalt2_e',
 'EX_cu2_e',
 'EX_k_e',
 'EX_mg2_e',
 'EX_mn2_e',
 'EX_o2_e',
 'EX_pi_e',
 'EX_zn2_e']

#%%
import pandas as pd
media = pd.read_csv('/Users/baeuerle/Organisation/Masterarbeit/refinegems/data/media_db.csv', sep=';')
#%%
M9 = media[media['medium']=='M9']
M9_ex = list('EX_' + M9['BiGG'] +'_e')

def remove_common(a, b):
  
    a, b = [i for i in a if i not in b], [j for j in b if j not in a]
  
    print("list1 : ", a)
    print("list2 : ", b)

print(a2_only)
remove_common(M9_ex, common)
remove_common(M9_ex, a1_only)
# for a2 there is missing ala_L_THr__L and salchs4fe in M9
# for a1 there is missing 'EX_chols_e', 'EX_ile__L_e', 'EX_istfrnA_e'

#%%
M9_paper = ['EX_ca2_e',
            'EX_cl_e',
            'EX_co2_e',
            'EX_cobalt2_e',
            'EX_cu2_e',
            'EX_fe2_e',	
            'EX_fe3_e',	
            'EX_glc__D_e',
            'EX_h2o_e',
            'EX_h_e',
            'EX_k_e',
            'EX_mg2_e',
            'EX_mn2_e',	
            'EX_mobd_e',
            #'EX_na1_e',
            'EX_nh4_e',
            #'EX_ni2_e',
            'EX_o2_e',
            'EX_pi_e',
            'EX_sel_e',
            'EX_slnt_e',
            'EX_so4_e',
            #'EX_tungs_e',
            'EX_zn2_e']
def find_exchanges(a):
    return a[:2] == 'EX'
M9_working = []
for i in M9_ex:
    try:
        model.reactions.get_by_id(i)
        M9_working.append(i)
    except (KeyError):
        print(str(i) + ' is not in model')
    
with model:
    #M9_working.extend(['EX_chols_e', 'EX_ile__L_e', 'EX_istfrnA_e'])
    for reaction in model.reactions:
        if 'EX' in str(reaction.id[:2]):
            reaction.lower_bound = 0
    #model.medium = {i:10.0 for i in M9_working}
    for id in M9_paper:#M9_working:
        model.reactions.get_by_id(id).lower_bound = -10
    model.reactions.get_by_id('EX_o2_e').lower_bound = -20
    #model.reactions.get_by_id('EX_glc__D_e').lower_bound = -20
    print(model.medium)
    sol = model.optimize()
    print(sol.objective_value)
    fluxes = pd.DataFrame(sol.fluxes)
    fluxes = fluxes.loc[fluxes['fluxes'] != 0].reset_index()
    print(fluxes.loc[fluxes['fluxes'] < 0].loc[fluxes['index'].apply(find_exchanges)])
    print(fluxes.loc[fluxes['fluxes'] > 0].loc[fluxes['index'].apply(find_exchanges)])
    # secretion of 4hba, co2, h2o, h, lac__L
    # https://www.megazyme.com/l-lactic-acid-assay-kit
    # ~option+n
    
#%%
RPMI_base = list('EX_' + media[media['medium']=='RPMI']['BiGG']+'_e')
RPMI = []
for i in RPMI_base:
    try:
        model.reactions.get_by_id(i)
        RPMI.append(i)
    except (KeyError):
        print(str(i) + ' is not in model')

with model:
    #RPMI.extend(common+a1_only)
    for reaction in model.reactions:
        if 'EX' in str(reaction.id[:2]):
            reaction.lower_bound = 0
    #model.medium = {i:10.0 for i in M9_working}
    for id in RPMI:#M9_working:
        model.reactions.get_by_id(id).lower_bound = -10
    model.reactions.get_by_id('EX_o2_e').lower_bound = -20
    #model.reactions.get_by_id('EX_glc__D_e').lower_bound = -20
    print(model.medium)
    sol = model.optimize()
    print(sol.objective_value)
    fluxes = pd.DataFrame(sol.fluxes)
    fluxes = fluxes.loc[fluxes['fluxes'] != 0].reset_index()
    #print(fluxes.loc[fluxes['fluxes'] < 0].loc[fluxes['index'].apply(find_exchanges)])
    print(fluxes.loc[fluxes['fluxes'] > 0].loc[fluxes['index'].apply(find_exchanges)])
    # https://www.megazyme.com/l-lactic-acid-assay-kit
    ess = []
    rmpi = common + a1_only
    for ex in rmpi:
        model.reactions.get_by_id(ex).lower_bound = -10
        if model.slim_optimize() > 0:
            ess.append(ex)
        model.reactions.get_by_id(ex).lower_bound = 0
    print(ess+RPMI)
    model.medium = {i:10 for i in ess+RPMI}
    print(model.optimize())

#%%   
def get_medium(media, name):
    RPMI_base = list('EX_' + media[media['medium']==name]['BiGG']+'_e')
    rpmi = []
    for i in RPMI_base:
        try:
            model.reactions.get_by_id(i)
            rpmi.append(i)
        except (KeyError):
            print(str(i) + ' is not in model')
    return rpmi

print(media)
medium = get_medium(media, 'SNM3')
with model:
    for reaction in model.reactions:
        if 'EX' in str(reaction.id[:2]):
            reaction.lower_bound = 0
    print(model.medium)
    model.medium = {i:10 for i in medium}
    print(model.medium)
    print(model.optimize())
    min_snm = minimal_medium(model, 0.1, minimize_components=True)
    minimal = list(pd.DataFrame(min_snm).reset_index()['index'])
    model.medium = {i:10 for i in minimal}
    print(model.medium)
    print(model.optimize())
    
#%%
# we have to look systematically at the flux distribution
m9 = get_medium(media, 'M9')
snm3 = get_medium(media, 'SNM3')
rpmi = get_medium(media, 'RPMI')

with model:
    model.medium = {i:10 for i in m9}
    print(model.medium)
    flux_m9 = pd.DataFrame(model.optimize().fluxes).rename({'fluxes':'fluxes_m9'}, axis=1)

with model:
    model.medium = {i:10 for i in snm3}
    print(model.medium)
    flux_snm3 = pd.DataFrame(model.optimize().fluxes).rename({'fluxes':'fluxes_snm3'}, axis=1)
    
with model:
    model.medium = {i:10 for i in rpmi}
    print(model.medium)
    flux_rpmi = pd.DataFrame(model.optimize().fluxes).rename({'fluxes':'fluxes_rpmi'}, axis=1)

#%%
all_flux = flux_rpmi.join(flux_m9).join(flux_snm3)
all_flux.loc[~(all_flux != 0).any(axis=1)] # 1578 reactions have no flux
all_flux.loc[(all_flux != 0).any(axis=1)] # only 428 have flux

#%%
model.optimize()
model.summary(fva=0.9)

#%%
import cobra
from refinegems import load_model_cobra
model = load_model_cobra('../models/Cstr_1115.xml')
model.optimize()
model.summary()

#%%
import pandas as pd
media = pd.read_csv('/Users/baeuerle/Organisation/Masterarbeit/refinegems/data/media_db.csv', sep=';')
#%%
M9 = media[media['medium']=='M9']
M9_ex = list('EX_' + M9['BiGG'] +'_e')
M9_ex.remove('EX_na1_e')
M9_ex.remove('EX_ni2_e')
M9_ex.remove('EX_glc__D_e')
#M9_ex.append('EX_cgly_e')
#M9_ex.append('EX_ala_B_e')
#M9_ex.append('EX_gly_cys__L_e') # same as cgly
#M9_ex.append('EX_glyc3p_e')
carbon_sources = ["EX_gly_e", 
                      "EX_fum_e", 
#                     "EX_male_e", 
                      "EX_pyr_e", 
                      "EX_succ_e", 
                      "EX_glc__D_e", 
                      "EX_urea_e", 
#                      "EX_22bipy_e",
#                      "EX_boricacid_e", 
#                      "EX_adocbl_e", 
#                      "EX_4abz_e", 
                      "EX_pnto__R_e", 
#                      "EX_pydam_e", 
#                      "EX_nac_e",
                      'EX_fru_e',
                      'EX_succ_e',
                      'EX_gam_e',
                      'EX_glyald_e',
                      'EX_malthp_e']
with model:
    model.medium = {i:10 for i in M9_ex}
    sol = model.optimize()
    print('no carbon' + ': ' + str(sol.objective_value))
    for s in carbon_sources:
        M9_ex.append(s)
        model.medium = {i:10 for i in M9_ex}
        sol = model.optimize()
        print(s + ': ' + str(sol.objective_value))
        M9_ex.remove(s)

# does not grow with 4abz, pnto__R, urea and gam

#%% growthmedia testing
model = load_model_cobra('../models/Cstr_TS.xml')
minimal = pd.read_csv('/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/analysis/minmal_media/Cstr_14_minmed.csv')
list(minimal['Unnamed: 0'])
#%%
M9 = media[media['medium']=='LB']
M9_ex = list('EX_' + M9['BiGG'] +'_e')
M9_ex.remove('EX_adn_e')
M9_ex.remove('EX_cbl1_e')
M9_ex.remove('EX_cd2_e')
M9_ex.remove('EX_cmp_e')
M9_ex.remove('EX_cro4_e')
M9_ex.remove('EX_dad_2_e')
M9_ex.remove('EX_gmp_e')
M9_ex.remove('EX_gsn_e')
M9_ex.remove('EX_hg2_e')
M9_ex.remove('EX_ins_e')
M9_ex.remove('EX_na1_e')
M9_ex.remove('EX_nac_e')
M9_ex.remove('EX_ni2_e')
M9_ex.remove('EX_pydx_e')
M9_ex.remove('EX_thymd_e')
M9_ex.remove('EX_ump_e')
M9_ex.remove('EX_uri_e')
print(M9_ex)
#M9_ex.remove('EX_glc__D_e')
with model:
    model.medium = {i:10 for i in M9_ex}
    sol = model.optimize().objective_value
    imp = []
    print(sol)
    min_ex = [i for i in list(minimal['Unnamed: 0']) if i not in M9_ex]
    for x in min_ex:
        model.reactions.get_by_id(x).lower_bound = - 10.0
        sol2 = model.optimize().objective_value
        print(sol2)
        if sol2 > sol:
            imp.append(x)
        model.reactions.get_by_id(x).lower_bound = 0
imp
    


