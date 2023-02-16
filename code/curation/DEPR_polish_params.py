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
modelpaths = ['../models/Cstr_TS.xml', '../models/Cstr_1197.xml', '../models/Cstr_1115.xml', '../models/Cstr_1116.xml']

for path in modelpaths:
    model = load_model_libsbml(path)
    for param in model.getListOfParameters():
        if param.isSetUnits() == False:
            param.setUnits('mmol_per_gDW_per_hr')
    writeSBMLToFile(model.getSBMLDocument(), path)
    
#%%
model = load_model_libsbml(modelpaths[0])
for reac in model.getListOfReactions():
    if reac.getPlugin('fbc').isSetLowerFluxBound():
        pass
    elif reac.getPlugin('fbc').isSetUpperFluxBound():
        pass
    else:
        print(reac.getId())


#%%
from bioservices import KEGG

k = KEGG()

#%%
rea2enz = k.link('enzyme','reaction')
enz2cst = k.link('cstr', 'enzyme')

#%%
import pandas as pd
data = pd.DataFrame([x.split('\t') for x in rea2enz.split('\n')]).rename({0:'Reactions', 1:'EC-Code'}, axis=1)
data
#%%
data2 = pd.DataFrame([x.split('\t') for x in enz2cst.split('\n')]).rename({1:'GPR', 0:'EC-Code'}, axis=1)
data2

dataf = data.merge(data2)

dataf.loc[dataf['Reactions'] == 'rn:R00859']

