""" First step to correct Biological Qualifier of CVTerms for KEGG Pathways in model KC-Na-01

From a earlier version of refineGEMs, KEGG pathways were added as BQB_IS
but the correct qualifier would be BQB_OCCURS_IN. This was only the case for KC-Na-01. 

This script will remove the kegg.pathway resource URI so that it can be added with the corrected script in refineGEMs.pathways.
"""

import refinegems as rg

__author__ = "Famke Baeuerle"

if __name__ == '__main__':

    mod = rg.io.load_model_libsbml('../models/Cstr_KC-Na-01.xml')

    for reac in mod.getListOfReactions():
        for cvs in reac.getCVTerms():
            for i in range(cvs.getNumResources()):
                uri = cvs.getResourceURI(i)
                if uri[24:36] == 'kegg.pathway':
                    cvs.removeResource(uri)

    rg.io.write_to_file(mod,'../models/Cstr_KC-Na-01.xml')
