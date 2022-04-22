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

#%%
# 04/04/22 Cstr_XX_charges.xml done with refinegems.charges
# 05/04/22 charge correction: look for metab without charges 
# 07/04/22 done to all models after gene polishing (Cstr_XX_genes.xml)

path = 'Cstr_17_genes.xml'

model = load_model_libsbml(path)
spe = model.getListOfSpecies()

# 05/04/22 correct charges in models, charges where ambig in ModelSEED but exact in BiGG
for i in spe:
    if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
        bigg = i.getId()[2:-2]
        if (bigg == '2ahbut'):
            print(bigg)
            charge = -1
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '3hocoa'):
            print(bigg)
            charge = -4
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'dhpmp'):
            print(bigg)
            charge = -2
            i.getPlugin('fbc').setCharge(int(charge))

# 05/04/22 manual correction because of list of charge unbalanced reactions (based on Cstr_17)
for i in spe:
    bigg = i.getId()[2:-2]
    if (bigg == '1p2cbxl'):
        print(bigg)
        charge = -1
        i.getPlugin('fbc').setCharge(int(charge))
    if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
        if (bigg == 'decoa'):
            print(bigg)
            charge = -4
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '4h2kpi'):
            print(bigg)
            charge = -2
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '4abzglu'):
            print(bigg)
            charge = -2
            i.getPlugin('fbc').setCharge(int(charge))

for i in spe:
    if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
        bigg = i.getId()[2:-2]
        if (bigg == '1ag160' 
            or bigg == '1ag180'
            or bigg == '1ag181d9'
            or bigg == '1ag182d9d12'
            or bigg == 'ala_L_thr__L'
            or bigg == 'ala_L_gln__L'
            or bigg == 'gly_gln__L'
            or bigg == 'ala_L_Thr__L'
            or bigg == 'nh3'
            or bigg == 'tag160'
            or bigg == 'dag181d9'
            or bigg == 'salchs4'
            or bigg == 'gly_pro__L'
            or bigg == 'gly_asn__L'
            or bigg == 'abg4'
            or bigg == 'istfrnA'
            or bigg == '2m35mdntha'
            or bigg == '35dnta'
            or bigg == 'metox'):
            print(bigg)
            charge = 0
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '2hetdp'
            or bigg == '3h4atb'
            or bigg == '3hasp__L'
            or bigg == 'R_3hdcaa'
            or bigg == 'mmalsa__S'
            or bigg == 'op4en'
            or bigg == '6atha'
            or bigg == 'gly_glu__L'
            or bigg == 'gly_asp__L'
            or bigg == '2hadnt'
            or bigg == '4hadnt'):
            print(bigg)
            charge = -1
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'istfrnB'
            ):
            print(bigg)
            charge = -2
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '2oxpaccoa'
            or bigg == '3h4atbcoa'
            or bigg == '3h6athcoa'
            or bigg == '3hbycoa'
            or bigg == '3hdd5coa'
            or bigg == '3hdd6coa'
            or bigg == '3hddccoa'
            or bigg == '3hdec4coa'
            or bigg == '3hhd58coa'
            or bigg == '3hhdccoa'
            or bigg == '3hhpcoa'
            or bigg == '3hnonacoa'
            or bigg == 'dd2coa'
            or bigg == 'tded5_2_coa'
            or bigg == '6athacoa'
            or bigg == '3hpbcoa'
            or bigg == '3hpdecacoa'
            or bigg == '3hphpcoa'
            or bigg == '3hphxacoa'
            or bigg == '3hpnonacoa'
            or bigg == '3hpoctacoa'
            or bigg == '6ath2coa'):
            print(bigg)
            charge = -4
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == '23dhacoa'):
            print(bigg)
            charge = -5
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'dscl'):
            print(bigg)
            charge = -7
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'salchs4fe'):
            print(bigg)
            charge = 3
            i.getPlugin('fbc').setCharge(int(charge))

new_document = model.getSBMLDocument()
writeSBMLToFile(new_document, path)
print("Polished model written to " + path)
test, errors = cobra.io.sbml.validate_sbml_model(path)
print(errors)

#%%
# download Pseudomonas putida and extract charges to add to Cstr
# 07/04/22: done to all models (after gene polishing with refinegems)

path = '../../Examples/iJN1463.xml'
model = load_model_libsbml(path)

path_to_change = 'Cstr_17_genes.xml'
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
            met = model.getSpecies('M_' + metab + comp)
            charge = met.getPlugin('fbc').getCharge()
            print('M_' + metab + comp, charge)
            met_to_change = model_to_change.getSpecies('M_' + metab + comp)
            met_to_change.getPlugin('fbc').setCharge(charge)
        except (AttributeError):
            print('M_' + metab + comp + ' does not exist in P. putida.')


writeSBMLToFile(new_document, path_to_change)
print("Polished model written to " + path_to_change)
test, errors = cobra.io.sbml.validate_sbml_model(path_to_change)
print(errors)

#%%
# 07/04/22 neue Runde charges setzen
# 07/04/22 basiert auf Cstr_17, über alle models laufen gelassen

path = 'Cstr_14_genes.xml'

model = load_model_libsbml(path)
spe = model.getListOfSpecies()

print(get_metab_without_charge(spe))

for i in spe:
    if not i.getPlugin('fbc').isSetCharge(): # we are only interested in metab without charge
        bigg = i.getId()[2:-2]
        if (bigg == 'actn__S' 
            or bigg == 'ala_L_his__L'
            or bigg == 'ala_L_leu__L'
            or bigg == 'alagly'
            or bigg == '4crsol'
            or bigg == 'stfrnB'
            or bigg == 'stfrnA'
            or bigg == 'hmbpp'
            or bigg == 'gly_phe__L'
            or bigg == 'glyglygln'
            or bigg == 'gly_tyr__L'
            or bigg == 'gly_met__L'
            or bigg == 'gly_leu__L'
            or bigg == 'gly_cys__L'
            or bigg == 'abg4'
            or bigg == 'istfrnA'
            or bigg == 'lysglugly'
            or bigg == 'prohisglu'
            or bigg =='serglugly'
            or bigg == 'nacg'
            or bigg == 'ala_L_gln__L'
            or bigg == 'abt__L'
            or bigg == 'm2bcoa'
            or bigg == 'ctncoa'
            or bigg == 'pppgpp'):
            print(bigg)
            charge = 0
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'ala_L_glu__L' 
            or bigg == 'pa160190'
            or bigg == 'pa190190'
            or bigg == 'lgt__S'
            or bigg == 'hethmpp'
            or bigg == 'met_L_ala__L'):
            print(bigg)
            charge = -1
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'ddcoa' 
            or bigg == 'nadphx__R'
            or bigg == 'nadphx__S'
            or bigg == 'mhpglu'
            or bigg == 'tagdp__D'):
            print(bigg)
            charge = -4
            i.getPlugin('fbc').setCharge(int(charge))
        if (bigg == 'nadhx__R' 
            or bigg == 'nadhx__S'
            or bigg == 'istfrnB'):
            print(bigg)
            charge = -2
            i.getPlugin('fbc').setCharge(int(charge))

writeSBMLToFile(new_document, path)
print("Polished model written to " + path)
test, errors = cobra.io.sbml.validate_sbml_model(path)
print(errors)

#%% schauen was noch fehlt an charges
path = 'Cstr_14_genes.xml'

model = load_model_libsbml(path)
spe = model.getListOfSpecies()

print(get_metab_without_charge(spe))
