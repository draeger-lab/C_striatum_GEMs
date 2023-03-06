""" Generate a core model using all strain specific models in this repository

This script will take all models present in the models folder (paths are hardcoded) and generates a core model. 
The core model is build from the reactions (and their respective metabolites with genes) that all models have in common and is thus prone to gaps.
The created core model will be polished and KEGG pathways are added as groups with a few functions from refineGEMs.

Note: This needs to be run with python3 code/curation/generate_coremodel.py from the C_striatum_GEMs folder. 
Can be run every time the models are changed that are used as input.
"""

import refinegems as rg
from cobra import Model, Reaction, Metabolite
from cobra.io import write_sbml_model, validate_sbml_model

__author__ = "Famke Baeuerle"

if __name__ == '__main__':

    modelpaths = [
        './models/Cstr_TS.xml', 
        './models/Cstr_1197.xml',
        './models/Cstr_1115.xml',
        './models/Cstr_1116.xml',
        './models/Cstr_KC-Na-01.xml',
        ]

    all_models = [rg.io.load_model_cobra(path) for path in modelpaths]

    all_reactions = {
        model.id: [re.id for re in model.reactions] for model in all_models
    }    

    print('Create core model of the models ' + ", ".join(list(all_reactions.keys())))
    
    set(all_reactions['fda_1054']).symmetric_difference(all_reactions['fda_1197']) #558
    set(all_reactions['fda_1197']).symmetric_difference(all_reactions['fda_1115']) #370
    set(all_reactions['fda_1197']).symmetric_difference(all_reactions['fda_1116']) #444

    common_rea = set(all_reactions['fda_1054']).intersection(all_reactions['fda_1116']).intersection(all_reactions['fda_1115']).intersection(all_reactions['fda_1197']).intersection(all_reactions['KC_Na_01'])

    core = Model('Cstr_core')
    for reac in common_rea:
        reaction = all_models[0].reactions.get_by_id(reac)
        core.add_reactions([reaction])

    reaction = all_models[0].reactions.get_by_id("Growth")
    core.add_reactions([reaction])
    core.reactions

    core.objective = 'Growth'
    
    print(f'Growth simulation of the core model yields growth rate {core.optimize().objective_value}')

    print(f'The new core model has {len(set(core.reactions) - set(core.boundary))} reactions and {len(set(core.boundary))} exchanges.')

    write_sbml_model(core, './models/Cstr_core.xml')
    print('Core model written to ./models/Cstr_core.xml')
    
    to_polish, _obs = rg.pathways.kegg_pathways('./models/Cstr_core.xml')
    rg.polish.add_fba_units(to_polish)
    rg.polish.set_default_units(to_polish)
    rg.polish.set_units(to_polish)
    rg.polish.add_compartment_structure_specs(to_polish)
    rg.polish.set_initial_amount(to_polish)
    rg.polish.polish_annotations(model=to_polish, new_pattern=True)
    rg.polish.change_all_qualifiers(model=to_polish, lab_strain=False)
    rg.io.write_to_file(to_polish, './models/Cstr_core.xml')
    mod, err = validate_sbml_model('./models/Cstr_core.xml')
    print(err)
    print(f'Core model is polished.')