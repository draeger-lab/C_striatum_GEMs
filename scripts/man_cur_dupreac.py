#%%
from libsbml import *
from numpy import NaN

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

#%%
# remove duplicate reactions (based on memote report)
sids_all = ['R_GLCNt2ir', 'R_ARGDI', 'R_ECOAH5_1', 'R_HACD1_1']
sids_17 = ['R_ECOAH5_1', 'R_ORNTAC_1', 'R_PPRGL']
sids_14 = ['R_ECOAH5_1', 'R_GLYCS_I', 'R_METSOX1abc']
sids_15 = ['R_GLYCS_I', 'R_ABTt_1']
sids_16 = ['OCBT_1']

mod_14 = load_model_libsbml('Cstr_14_dupreac.xml')
reac_14 = mod_14.getListOfReactions()
mod_15 = load_model_libsbml('Cstr_15_dupreac.xml')
reac_15 = mod_15.getListOfReactions()
mod_16 = load_model_libsbml('Cstr_16_dupreac.xml')
reac_16 = mod_16.getListOfReactions()
mod_17 = load_model_libsbml('Cstr_17_dupreac.xml')
reac_17 = mod_17.getListOfReactions()

def remove_duplicates(reac, sids):
    for sid in sids:
        if reac.getElementBySId(sid) is not None:
            print(str(reac.getElementBySId(sid)) + ' found.')
            reac.remove(sid)
            print(sid + ' removed.')

remove_duplicates(reac_14, sids_all)
remove_duplicates(reac_14, sids_14)
remove_duplicates(reac_15, sids_all)
remove_duplicates(reac_15, sids_15)
remove_duplicates(reac_16, sids_all)
remove_duplicates(reac_16, sids_16)
remove_duplicates(reac_17, sids_all)
remove_duplicates(reac_17, sids_17)

writeSBMLToFile(mod_14.getSBMLDocument(),'Cstr_14_dupreac.xml')
writeSBMLToFile(mod_15.getSBMLDocument(),'Cstr_15_dupreac.xml')
writeSBMLToFile(mod_16.getSBMLDocument(),'Cstr_16_dupreac.xml')
writeSBMLToFile(mod_17.getSBMLDocument(),'Cstr_17_dupreac.xml')