# from Hawkey 2022
import cobra
import pandas as pd
from cobra.io import load_json_model
from glob import glob
from argparse import ArgumentParser
import os

def get_arguments():
    parser = ArgumentParser(description='Growth simulations for models')

    # job submission options
    parser.add_argument('--model', required=True, help='Model file to simulate')
    parser.add_argument('--prefix', required=True, help='Prefix for output files')
    parser.add_argument('--media', required=False, default='m9', help='Use different media to optimise your models. Options are m9 (default), or '
                                                                        'm9_leu (for Shigella sonnei)')

    return parser.parse_args()

def m9(model):
    for reaction in model.reactions:
        if 'EX_' in reaction.id:
            reaction.lower_bound=0
    model.reactions.EX_ca2_e.lower_bound=-1000
    model.reactions.EX_cl_e.lower_bound=-1000
    model.reactions.EX_co2_e.lower_bound=-1000
    model.reactions.EX_cobalt2_e.lower_bound=-1000
    model.reactions.EX_cu2_e.lower_bound=-1000
    model.reactions.EX_fe2_e.lower_bound=-1000
    model.reactions.EX_fe3_e.lower_bound=-1000
    model.reactions.EX_h_e.lower_bound=-1000
    model.reactions.EX_h2o_e.lower_bound=-1000
    model.reactions.EX_k_e.lower_bound=-1000
    model.reactions.EX_mg2_e.lower_bound=-1000
    model.reactions.EX_mn2_e.lower_bound=-1000
    model.reactions.EX_mobd_e.lower_bound=-1000
    #model.reactions.EX_na1_e.lower_bound=-1000 # off for 14, 15, 16, 17, KC
    #model.reactions.EX_tungs_e.lower_bound=-1000 # off for 14, 15, 16, 17, KC
    model.reactions.EX_zn2_e.lower_bound=-1000
    #model.reactions.EX_ni2_e.lower_bound=-1000 # off for 14, 15, 16, 17, KC
    #model.reactions.EX_sel_e.lower_bound=-1000 # off for 15, 16, 17, KC
    #model.reactions.EX_slnt_e.lower_bound=-1000 # off for 15, 16, 17, KC
    model.reactions.EX_glc__D_e.lower_bound=-20
    model.reactions.EX_so4_e.lower_bound=-1000
    model.reactions.EX_nh4_e.lower_bound=-1000
    model.reactions.EX_pi_e.lower_bound=-1000
    #model.reactions.EX_cbl1_e.lower_bound=-.01 # off for 14, 15, 16, 17, KC
    model.reactions.EX_o2_e.lower_bound=-20
    #model.reactions.EX_ala_B_e.lower_bound=-1000 # for 15 (minimal requirement)
    #model.reactions.EX_cgly_e.lower_bound=-1000 # for 15, 16 (minimal requirement)
    model.reactions.EX_pnto__R_e.lower_bound=-1000 # for 16, 17 (minimal requirement)
    model.reactions.EX_nmn_e.lower_bound=-1000 # for 17 (minimal requirement)
    return model

def m9_leu(model):
    for reaction in model.reactions:
        if 'EX_' in reaction.id:
            reaction.lower_bound=0
    model.reactions.EX_ca2_e.lower_bound=-1000
    model.reactions.EX_cl_e.lower_bound=-1000
    model.reactions.EX_co2_e.lower_bound=-1000
    model.reactions.EX_cobalt2_e.lower_bound=-1000
    model.reactions.EX_cu2_e.lower_bound=-1000
    model.reactions.EX_fe2_e.lower_bound=-1000
    model.reactions.EX_fe3_e.lower_bound=-1000
    model.reactions.EX_h_e.lower_bound=-1000
    model.reactions.EX_h2o_e.lower_bound=-1000
    model.reactions.EX_k_e.lower_bound=-1000
    model.reactions.EX_mg2_e.lower_bound=-1000
    model.reactions.EX_mn2_e.lower_bound=-1000
    model.reactions.EX_mobd_e.lower_bound=-1000
    model.reactions.EX_na1_e.lower_bound=-1000
    model.reactions.EX_tungs_e.lower_bound=-1000
    model.reactions.EX_zn2_e.lower_bound=-1000
    model.reactions.EX_ni2_e.lower_bound=-1000
    model.reactions.EX_sel_e.lower_bound=-1000
    model.reactions.EX_slnt_e.lower_bound=-1000
    model.reactions.EX_glc__D_e.lower_bound=-20
    model.reactions.EX_so4_e.lower_bound=-1000
    model.reactions.EX_nh4_e.lower_bound=-1000
    model.reactions.EX_pi_e.lower_bound=-1000
    model.reactions.EX_cbl1_e.lower_bound=-.01
    model.reactions.EX_o2_e.lower_bound=-20
    model.reactions.EX_leu__L_e.lower_bound=-1000
    return model

# define a function to simulate growth on any of the four possible source types
def simulate_growth(list_of_sources, strainIDs, model, media_type, source_type = 'C'):
    mod = load_json_model(model)
    growthCapabilities=pd.DataFrame(index=list_of_sources,columns=strainIDs)
    # determine what the default source is that we need to close
    if source_type == 'C':
        default_type = 'EX_glc__D_e'
    elif source_type == 'N':
        default_type = 'EX_nh4_e'
    elif source_type == 'P':
        default_type = 'EX_pi_e'
    elif source_type == 'S':
        default_type = 'EX_so4_e'
    # iterate through all the models to simulate growth on different sources
    listCapabilities=[]

    for source in list_of_sources:
        # put in the correct media
        if media_type == 'm9':
            m9(mod)
        elif media_type == 'm9_leu':
            m9_leu(mod)
        # close the default source by setting the lower bound of its exchange reaction to 0,
        # and open the exchange reaction of the source of interest to enable nutrient update
        mod.reactions.get_by_id(default_type).lower_bound=0
        mod.reactions.get_by_id(source).lower_bound=-1000
        listCapabilities.append(mod.optimize().objective_value)

    for col in growthCapabilities.columns:
        if col in model:
            growthCapabilities[col]=listCapabilities

    return(growthCapabilities)

def get_reactions(model, source):
    source_list = []
    for r in model.reactions:
        if 'EX_' in r.id:
            for m in r.metabolites:
                if source in m.formula:
                    source_list.append(r.id)
    return(source_list)

def get_all_reactions(model):
    carbon_sources=get_reactions(model, 'C')
    nitrogen_sources = get_reactions(model, 'N')
    phos_sources = get_reactions(model, 'P')
    sulfur_sources = get_reactions(model, 'S')

    return(carbon_sources, nitrogen_sources, phos_sources, sulfur_sources)

def simulate_growth_all(model_file, out_prefix, media_type):

    # make lists of the different source types
    print('Get list of reactions for each source type...')
    mod_in = load_json_model(model_file)

    carbon_sources, nitrogen_sources, phos_sources, sulfur_sources = get_all_reactions(mod_in)

    # get the name of the strain/strains for the output files
    strainIDs = []
    basename = os.path.basename(model_file)
    id = os.path.splitext(basename)[0]
    strainIDs.append(id)

    # simulate growth on different sources
    print('Calculate carbon capabilities...')
    carbon_capabilities = simulate_growth(carbon_sources, strainIDs, model_file, media_type, source_type='C')
    carbon_capabilities.to_csv(out_prefix + '_carbon_sources.tsv', sep='\t')
    print('Calculate nitrogen capabilities...')
    nitrogen_capabilities = simulate_growth(nitrogen_sources, strainIDs, model_file, media_type, source_type='N')
    nitrogen_capabilities.to_csv(out_prefix + '_nitrogen_sources.tsv', sep='\t')
    print('Calculate phosphorus capabilities...')
    phos_capabilities = simulate_growth(phos_sources, strainIDs, model_file, media_type, source_type='P')
    phos_capabilities.to_csv(out_prefix + '_phos_sources.tsv', sep='\t')
    print('Calculate sulfur capabilities...')
    sulfur_capabilities = simulate_growth(sulfur_sources, strainIDs, model_file, media_type, source_type='S')
    sulfur_capabilities.to_csv(out_prefix + '_sulfur_sources.tsv', sep='\t')

def main():

    args = get_arguments()

    simulate_growth_all(args.model, args.prefix, args.media)

if __name__ == '__main__':
    main()
    # python3 simulate_growth_single.py --model /Users/baeuerle/Organisation/Masterarbeit/C_striatum_GEMs/escher/Cstr_16.json --prefix ../analysis/hawkey/Cstr_16
