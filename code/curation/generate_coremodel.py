"""_summary_
"""

import refinegems as rg
from cobra import Model, Reaction, Metabolite
from cobra.io import write_sbml_model

__author__ = "Famke Baeuerle"

if __name__ == '__main__':

    modelpaths = [
        '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_14.xml', 
        '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_15.xml',
        '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_16.xml',
        '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_17.xml',
        '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_KC-Na-01.xml',
        ]

    all_models = [rg.io.load_model_cobra(path) for path in modelpaths]

    all_reactions = {
        model.id: [re.id for re in model.reactions] for model in all_models
    }    

    print('Create core model of the models ' + str(all_reactions.keys()))
    
    set(all_reactions['fda_1054']).symmetric_difference(all_reactions['fda_1197']) #558
    set(all_reactions['fda_1197']).symmetric_difference(all_reactions['fda_1115']) #370
    set(all_reactions['fda_1197']).symmetric_difference(all_reactions['fda_1116']) #444

    common_rea = set(all_reactions['fda_1054']).intersection(all_reactions['fda_1116']).intersection(all_reactions['fda_1115']).intersection(all_reactions['fda_1197'])

    core = Model('Cstr_core')
    for reac in common_rea:
        reaction = all_models[0].reactions.get_by_id(reac)
        core.add_reactions([reaction])

    reaction = all_models[0].reactions.get_by_id("Growth")
    core.add_reactions([reaction])
    core.reactions

    core.objective = 'Growth'
    
    print(f'Growth simulation of the core model yields {core.optimize()}')

    print(f'The new core model has {len(set(core.reactions) - set(core.boundary))} reactions and {len(set(core.boundary))} exchanges.')


    write_sbml_model(core, '/Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/models/Cstr_core.xml')