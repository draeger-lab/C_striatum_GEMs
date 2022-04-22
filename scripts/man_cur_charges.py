#%%
from libsbml import *
import cobra

def load_model_libsbml(modelpath):
    """loads model using libsbml

    Args:
        modelpath (Str): Path to GEM

    Returns:
        libsbml-model: loaded model by libsbml
    """
    reader = SBMLReader()
    read = reader.readSBMLFromFile(modelpath) #read from file
    mod = read.getModel()
    return mod

def get_metab_without_charge(metab_list):
    uncharged = []
    for i in spe:
        bigg = i.getId()[2:-2]
        if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
            if bigg not in uncharged:
                uncharged.append(bigg)
    return uncharged

#%% add charges from Pseudomonas putida to Cstr

example_path = '../../Nextcloud/Examples/iJN1463.xml'
example_model = load_model_libsbml(example_path)
print(example_model.getId())

modelpaths_to_change = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']

for path_to_change in modelpaths_to_change:
    model_to_change = load_model_libsbml(path_to_change)
    spe = model_to_change.getListOfSpecies()
    uncharged_to_change = []
    
    for i in spe:
        bigg = i.getId()[2:-2]
        if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
            if bigg not in uncharged_to_change:
                uncharged_to_change.append(bigg)

    for metab in uncharged_to_change:
        compart = ['_c', '_p', '_e']
        for comp in compart:
            try:
                met = example_model.getSpecies('M_' + metab + comp)
                charge = met.getPlugin('fbc').getCharge()
                print('M_' + metab + comp, charge)
                met_to_change = model_to_change.getSpecies('M_' + metab + comp)
                met_to_change.getPlugin('fbc').setCharge(charge)
            except (AttributeError):
                print('M_' + metab + comp + ' does not exist in P. putida.')


    writeSBMLToFile(model_to_change.getSBMLDocument(),path_to_change)
    print("Polished model written to " + path_to_change)
    test, errors = cobra.io.sbml.validate_sbml_model(path_to_change)
    print(errors)

#%% see which metabolites are still uncharged
path = '../models/Cstr_14_genes.xml'
model = load_model_libsbml(path)
print(get_metab_without_charge(model.getListOfSpecies()))

#%% add charges from manually curated lists of metabolites
zero = ['actn__S' , 'ala_L_his__L', 'ala_L_leu__L', 'alagly', '4crsol', 'stfrnB', 'stfrnA', 'hmbpp', 'gly_phe__L', 'glyglygln', 'gly_tyr__L', 'gly_met__L'
, 'gly_leu__L', 'gly_cys__L', 'abg4', 'istfrnA', 'lysglugly', 'prohisglu', 'serglugly', 'nacg', 'ala_L_gln__L', 'abt__L', 'm2bcoa', 'ctncoa', 'pppgpp', '1ag160' 
, '1ag180', '1ag181d9', '1ag182d9d12', 'ala_L_thr__L', 'ala_L_gln__L', 'gly_gln__L', 'ala_L_Thr__L', 'nh3', 'tag160', 'dag181d9', 'salchs4', 'gly_pro__L'
, 'gly_asn__L', 'abg4', 'istfrnA', '2m35mdntha', '35dnta', 'metox']
minus_1 = ['2ahbut', 'ala_L_glu__L', 'pa160190', 'pa190190', 'lgt__S', 'hethmpp', 'met_L_ala__L', '2ahbut', '2hetdp', '3h4atb', '3hasp__L', 'R_3hdcaa'
, 'mmalsa__S', 'op4en', '6atha', 'gly_glu__L', 'gly_asp__L', '2hadnt', '4hadnt', '1p2cbxl']
minus_2 = ['nadhx__R', 'nadhx__S', 'istfrnB', 'dhpmp', '4h2kpi', '4abzglu']
minus_4 = ['ddcoa', 'nadphx__R', 'nadphx__S', 'mhpglu', 'tagdp__D', '2oxpaccoa', '3h4atbcoa', '3h6athcoa', '3hbycoa', '3hdd5coa', '3hdd6coa', '3hddccoa'
, '3hdec4coa', '3hhd58coa', '3hhdccoa', '3hhpcoa', '3hnonacoa', 'dd2coa', 'tded5_2_coa', '6athacoa', '3hpbcoa', '3hpdecacoa', '3hphpcoa', '3hphxacoa'
, '3hpnonacoa', '3hpoctacoa', '6ath2coa', '3hocoa', 'decoa']
minus_5 = ['23dhacoa']
minus_7 = ['dscl']
plus_3 = ['salchs4fe']

charges = {0: zero, -1 : minus_1, -2 : minus_2, -4: minus_4, -5 : minus_5, 
           -7 : minus_7, 3: plus_3}

modelpaths = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']

def key_return(X):
    for key, value in charges.items():
        if X == value:
            return key
        if isinstance(value, list) and X in value:
            return key
    return 1000

for path in modelpaths:
    model = load_model_libsbml(path)
    spe = model.getListOfSpecies()

    for metabolite in spe:
        #if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
        bigg = metabolite.getId()[2:-2]
        charge = key_return(bigg)
        if charge < 1000:
            print(bigg, charge)
            metabolite.getPlugin('fbc').setCharge(int(charge))

    writeSBMLToFile(model.getSBMLDocument(),path)
    print("Polished model written to " + path)
    test, errors = cobra.io.sbml.validate_sbml_model(path)
    print(errors)
    
