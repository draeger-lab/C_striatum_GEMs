# from a earlier version of refineGEMs, KEGG pathways were added as bqb is 
# but it needs to be bqb occurs in
# this is only the case for KC-Na-01 

#%%
import refinegems as rg

mod = rg.load.load_model_libsbml('../models/Cstr_KC-Na-01.xml')

#%%
for reac in mod.getListOfReactions():
    for cvs in reac.getCVTerms():
        for i in range(cvs.getNumResources()):
            uri = cvs.getResourceURI(i)
            if uri[24:36] == 'kegg.pathway':
                cvs.removeResource(uri)

rg.load.write_to_file(mod,'../models/Cstr_KC-Na-01.xml')
