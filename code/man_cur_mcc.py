#%%
import MCC
from MCC import MassChargeCuration
import pandas as pd
model_path = '../models/Cstr_17.xml'
#%%
balancer = MassChargeCuration(model_path, run_optimization = True, update_ids = True, data_path='../data/mcc/') #
#%%
balancer.generate_visual_report().show()
#%%
metabolite_report_df = balancer.generate_metabolite_report()
metabolite_report_df[::200]
#%%
metabolite_report_df[metabolite_report_df["Similarity"] != "Same"]
#%%
metabolite_report_df[metabolite_report_df["Used Databases"] == ""]
#%%
balancer.model_interface.write_model(model_path)
#%%
balancer.generate_visual_report(f"Cstr_17_visual")
balancer.generate_metabolite_report(f"Cstr_17_metabolites")
balancer.generate_reaction_report(f"Cstr_17_reactions")