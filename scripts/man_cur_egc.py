#%%
import cobra
import pandas as pd

model = cobra.io.read_sbml_model('../models/Cstr_14.xml')
model

#%%
dissipation_rxns = pd.read_csv("../data/energy_dissipation_rxns.csv")
dissipation_rxns 

#%%
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
from cobra import Reaction
import numpy as np

#simulate changed conditions without changing the entire model
with model: 
    # add dissipation reactions
    model.reactions.get_by_id('SIRA2').remove_from_model()
    model.reactions.get_by_id('FPRA').remove_from_model()
    model.reactions.get_by_id('GCDH').remove_from_model()
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
            df.to_csv('../escher/fba/Cstr_14_' + str(row['type']) + '.csv')
#%%
def metabolite_flux_balance(metabolite, solution):
    """
    Return a vector of reaction fluxes scaled by the stoichiometric coefficient.

    Parameters
    ----------
    metabolite : cobra.Metabolite
        The metabolite whose fluxes are to be investigated.
    solution : cobra.Solution
        Solution with flux values.

    Returns
    -------
    pandas.Series
        A vector with fluxes of reactions that consume or produce the given
        metabolite scaled by the corresponding stoichiometric coefficients. The
        reaction identifiers are given by the index.
    """
    rxn_ids = list()
    adj_flux = list()
    for rxn in metabolite.reactions:
        coef = rxn.get_coefficient(metabolite)
        rxn_ids.append(rxn.id)
        adj_flux.append(coef * solution.fluxes[rxn.id])
    return pd.Series(data=adj_flux, index=rxn_ids, dtype=float, name="reaction")
#%%
model.metabolites.get_by_id("akg_c")
#model.reactions.get_by_id("FDMOtau")

#%%
atp_flux = metabolite_flux_balance(model.metabolites.atp_c, model.optimize())
influx = atp_flux[atp_flux > 0.0].sum()
atp_flux

#%%
met = 'glu__L_c'
for rea in model.metabolites.get_by_id(met).reactions:
    for prod in rea.products:
        if prod == model.metabolites.get_by_id(met):
            print(rea)

#%%
#Solve
solution = model.optimize() #solution is stored at model.solution
#Output solution
print('Growth Rate: '+str(solution.objective_value)+' 1/h')
print(solution.fluxes)
df=pd.DataFrame.from_dict([solution.fluxes]).T
df.to_csv('../escher/Cstr_14_FBA.csv')
# %%

model = cobra.io.read_sbml_model('../models/Cstr_15.xml')
try: 
    model.reactions.get_by_id('SIRA2').remove_from_model(remove_orphans=True)
    model.reactions.get_by_id('FPRA').remove_from_model(remove_orphans=True)
    model.reactions.get_by_id('GCDH').remove_from_model(remove_orphans=True)
except (KeyError):
    pass
cobra.io.write_sbml_model(model, '../models/Cstr_15.xml')
# %%

modelpaths = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']

for path in modelpaths:
    model = cobra.io.read_sbml_model(path)
    try: 
        model.reactions.get_by_id('SIRA2').remove_from_model(remove_orphans=True)
        model.reactions.get_by_id('FPRA').remove_from_model(remove_orphans=True)
        model.reactions.get_by_id('GCDH').remove_from_model(remove_orphans=True)
    except (KeyError):
        pass
    cobra.io.write_sbml_model(model, path)   
