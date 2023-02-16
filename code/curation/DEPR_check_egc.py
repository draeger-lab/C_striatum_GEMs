#%%
import cobra
import pandas as pd
import numpy as np
from cobra import Reaction

# input : reaction string
# output : {<Metabolite object> : stoichiometry (integer)}
# this method is only useful, if coefficients are either 1 or 2 
def parse_reaction(eq):
    eq = eq.split(' ')
    eq_matrix={}
    
    are_products = False
    coeff = 1
    for i,part in enumerate(eq):
        if part == '-->':
            are_products = True
            continue          
        if part == '+':
            continue
        if part == '2':
            coeff = 2
            continue
        if are_products:
            eq_matrix[model.metabolites.get_by_id(part)] = 1*coeff
            coeff = 1
        else:
            eq_matrix[model.metabolites.get_by_id(part)] = -1*coeff
            coeff = 1
    return eq_matrix
#%%
model = cobra.io.read_sbml_model('../models/Cstr_TS.xml')
dissipation_rxns = pd.read_csv("../data/energy_dissipation_rxns.csv")
dissipation_rxns
#%%
#simulate changed conditions without changing the entire model
with model: 
    # add dissipation reactions
    for i, row in dissipation_rxns.iterrows():
        met_atp = parse_reaction(row['equation'])
        rxn = Reaction(row['type'])
        rxn.name = 'Test ' + row['type'] + ' dissipation reaction'
        rxn.add_metabolites(met_atp)
        model.add_reaction(rxn)
        
    for rxn in model.reactions:
        if 'EX_' in rxn.id:
            rxn.upper_bound = 0.0
            rxn.lower_bound = 0.0
            #print('Set exchange rxn to 0', rxn.name)
        # set reversible reactions fluxes to [-1,1]    
        elif rxn.reversibility: 
            rxn.upper_bound = 1.0
            rxn.lower_bound = -1.0
            #print('Reversible rxn', rxn.name)
        # irreversible reactions have fluxes [0.1]    
        else:
            rxn.upper_bound = 1.0
            rxn.lower_bound = 0.0
            #print('Irreversible rxn', rxn.name)

    # optimize by choosing one of dissipation reactions as an objective
    for i, row in dissipation_rxns.iterrows():
        model.objective = row['type']
        print('Set objective to', row['type'], ':', model.optimize().objective_value)
        if model.optimize().objective_value > 0.0:
            df=pd.DataFrame.from_dict([model.optimize().fluxes]).T.replace(0, np.nan).dropna(axis=0)
            df.to_csv('../escher/egc/Cstr_14_' + str(row['type']) + '.csv')

# %%
# remove the suspicious reactions
modelpaths = ['../models/Cstr_TS.xml', '../models/Cstr_1197.xml', '../models/Cstr_1115.xml', '../models/Cstr_1116.xml']

for path in modelpaths:
    model = cobra.io.read_sbml_model(path)
    try: 
        model.reactions.get_by_id('SIRA2').remove_from_model(remove_orphans=True)
        model.reactions.get_by_id('FPRA').remove_from_model(remove_orphans=True)
        model.reactions.get_by_id('GCDH').remove_from_model(remove_orphans=True)
    except (KeyError):
        pass
    cobra.io.write_sbml_model(model, path)
    
#%%
# test other models for EGC
modelpaths = ['../models/Cstr_1197.xml', '../models/Cstr_1115.xml', '../models/Cstr_1116.xml']
dissipation_rxns = dissipation_rxns.drop(11)
for path in modelpaths:
    model = cobra.io.read_sbml_model(path)
    with model: 
    # add dissipation reactions
        for i, row in dissipation_rxns.iterrows():
            met_atp = parse_reaction(row['equation'])
            rxn = Reaction(row['type'])
            rxn.name = 'Test ' + row['type'] + ' dissipation reaction'
            rxn.add_metabolites(met_atp)
            model.add_reaction(rxn)
            
        for rxn in model.reactions:
            if 'EX_' in rxn.id:
                rxn.upper_bound = 0.0
                rxn.lower_bound = 0.0
                #print('Set exchange rxn to 0', rxn.name)
            # set reversible reactions fluxes to [-1,1]    
            elif rxn.reversibility: 
                rxn.upper_bound = 1.0
                rxn.lower_bound = -1.0
                #print('Reversible rxn', rxn.name)
            # irreversible reactions have fluxes [0.1]    
            else:
                rxn.upper_bound = 1.0
                rxn.lower_bound = 0.0
                #print('Irreversible rxn', rxn.name)
        
        try: 
            model.reactions.get_by_id('SIRA2').remove_from_model(remove_orphans=True)
            model.reactions.get_by_id('FPRA').remove_from_model(remove_orphans=True)
            model.reactions.get_by_id('GCDH').remove_from_model(remove_orphans=True)
        except (KeyError):
            pass

        # optimize by choosing one of dissipation reactions as an objective
        for i, row in dissipation_rxns.iterrows():
            model.objective = row['type']
            print('Set objective to', row['type'], ':', model.optimize().objective_value)
            if model.optimize().objective_value > 0.0:
                df=pd.DataFrame.from_dict([model.optimize().fluxes]).T.replace(0, np.nan).dropna(axis=0)
                #df.to_csv('../escher/fba/Cstr_14_' + str(row['type']) + '.csv')
                print(df)
                
# no EGC detected
