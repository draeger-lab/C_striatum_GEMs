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

#%%
import sqlite3
import pandas as pd

con = sqlite3.connect("../../Databases/bigg.sqlite")

#%%
cur = con.cursor()
    
df = pd.read_sql_query("SELECT * from model_reaction", con)
df3 = pd.read_sql_query("SELECT * from model", con)

df2 = pd.read_sql_query("SELECT * from reaction", con)
df4 = df2.rename({'id': 'reaction_id'}, axis=1).merge(df)

df3.rename({'id': 'model_id', 'bigg_id': 'bigg_model_id'}, axis=1).merge(df4)
df5 = pd.read_sql_query("SELECT * from complex_composition", con)
df5