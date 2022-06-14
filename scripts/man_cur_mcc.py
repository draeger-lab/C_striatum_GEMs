#%%
import MCC
from MCC import MassChargeCuration
import cobra
import pandas as pd
model_path = '../models/Cstr_14.xml'
#model = cobra.io.read_sbml_model(model_path)
#model
#%%
balancer = MassChargeCuration(model_path, update_ids = True,run_optimization = True, data_path='../data/mcc/')
#%%
balancer.generate_visual_report().show()
#%%


metabolite_report_df = balancer.generate_metabolite_report()
metabolite_report_df[::200]

metabolite_report_df[metabolite_report_df["Similarity"] != "Same"]
#%%
metabolite_report_df[metabolite_report_df["Used Databases"] == ""]

#%%
balancer.model_interface.write_model(model_path)

#%%
balancer.generate_visual_report(f"Cstr_14_visual")
balancer.generate_metabolite_report(f"Cstr_14_metabolites")
balancer.generate_reaction_report(f"Cstr_14_reactions")