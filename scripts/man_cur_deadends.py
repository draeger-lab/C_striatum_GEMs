#%%
import cobra
modelpath = '../models/Cstr_15.xml'
model = cobra.io.read_sbml_model(modelpath)

#%%
model.metabolites.get_by_any('spmd_c')[0]

model.reactions.get_by_any('SPMS')[0].lower_bound = -1000.0
#model.reactions.get_by_any('SPMDabc')[0]
#model.reactions.get_by_any('SPMDt3i')[0]

model.reactions.get_by_any('SPMS')[0]

#%%
model.metabolites.get_by_any('so3_c')[0]
model.reactions.get_by_any('SIRA2')[0]
#%%
from libsbml import *

reader = SBMLReader()
read = reader.readSBMLFromFile(modelpath) #read from file
mod = read.getModel()

#%%
mod.getListOfSpecies().getElementBySId('M_spmd_c') 
mod.getListOfReactions().getElementBySId('R_SPMS').getReversible()
# this reaction has to be reversible according to MetaCyc and Rhea