#%%
from libsbml import *

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
modelpaths = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']

for path in modelpaths:
    model = load_model_libsbml(path)
    for param in model.getListOfParameters():
        if param.isSetUnits() == False:
            param.setUnits('mmol_per_gDW_per_hr')
    writeSBMLToFile(model.getSBMLDocument(), path)
