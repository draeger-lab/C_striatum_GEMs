# from Hawkey 2022
import cobra
from cobra.io import load_json_model
from cobra.flux_analysis import single_gene_deletion
import pandas as pd
from argparse import ArgumentParser

# single_gene_knockouts | single gene knockouts in M9+glucose | possible | Hawkey et al., 2022

def get_arguments():
    parser = ArgumentParser(description='Conduct single gene knockouts in M9+glucose for each model')

    # job submission options
    parser.add_argument('--models', nargs='+', type=str, required=True, help='list of model files to analyse')
    parser.add_argument('--gene_matrix', type=str, required=True, help='Gene matrix that matches model genes to master model genes')
    parser.add_argument('--out', type=str, required=True, help='prefix for output file')

    return parser.parse_args()

def m9(model):
    for reaction in model.reactions:
        if 'EX_' in  reaction.id:
            reaction.lower_bound=0
    model.reactions.EX_ca2_e.lower_bound=-1000
    model.reactions.EX_cl_e.lower_bound=-1000
    model.reactions.EX_co2_e.lower_bound=-1000
    model.reactions.EX_cobalt2_e.lower_bound=-1000
    model.reactions.EX_cu2_e.lower_bound=-1000
    model.reactions.EX_fe2_e.lower_bound=-1000
    model.reactions.EX_fe3_e.lower_bound=-1000
    model.reactions.EX_h_e.lower_bound=-1000
    model.reactions.EX_h2o_e.lower_bound=-1000
    model.reactions.EX_k_e.lower_bound=-1000
    model.reactions.EX_mg2_e.lower_bound=-1000
    model.reactions.EX_mn2_e.lower_bound=-1000
    model.reactions.EX_mobd_e.lower_bound=-1000
    model.reactions.EX_na1_e.lower_bound=-1000
    model.reactions.EX_tungs_e.lower_bound=-1000
    model.reactions.EX_zn2_e.lower_bound=-1000
    model.reactions.EX_ni2_e.lower_bound=-1000
    model.reactions.EX_glc__D_e.lower_bound=-20
    model.reactions.EX_so4_e.lower_bound=-1000
    model.reactions.EX_nh4_e.lower_bound=-1000
    model.reactions.EX_pi_e.lower_bound=-1000
    model.reactions.EX_cbl1_e.lower_bound=-.01
    model.reactions.EX_o2_e.lower_bound=-20
    return model

def main():

    args = get_arguments()

    # read in the gene matrix
    gene_matrix = pd.read_csv(args.gene_matrix)
    # rename first column
    gene_matrix.rename(columns={'Unnamed: 0':'master_gene'}, inplace=True)
    # get list of genes
    gene_ids = list(gene_matrix['master_gene'])
    # initialise final dict of results - key is master model gene, value is 0/1 for
    # growth or not in that strain
    # so if a master model gene isn't in a strain, need to record 'NA'
    final_dict = {}
    for gene in gene_ids:
        final_dict[gene] = []

    # set up a list to record all the model file names for column headers later
    model_file_names = []
    for model in args.models:
        # read in the model, intialise in m9 and perform single gene deletions
        model_in = load_json_model(model)
        model_file_names.append(model_in.id)
        m9(model_in)
        deletion_results = single_gene_deletion(model_in)
        # get out list of genes from model - need to convert from frozen set to single list of genes
        model_genes = [list(x) for x in deletion_results.index]
        model_genes = sum(model_genes, [])
        # add this as a new column to the deletion results
        deletion_results['geneIDs'] = model_genes
        # add a new column to deletion results that matches the genes to the master model
        model_gene_match = gene_matrix[['master_gene', model_in.id]]
        # add to deletion results
        model_gene_match = model_gene_match.rename(columns={model_in.id: 'geneIDs'})
        combined_results = deletion_results.merge(model_gene_match, on='geneIDs', how='inner')
        for index,row in combined_results.iterrows():
            # if growth is high, count as a 1
            if row.growth > 0.0001:
                final_dict[row.master_gene].append(1)
            # otherwise 0
            else:
                final_dict[row.master_gene].append(0)
        # check for any genes that aren't in the model, add NAs for those
        for gene in gene_ids:
            if gene not in list(combined_results.master_gene):
                final_dict[gene].append('NA')

    # we want our output to have master model genes as COLUMNS
    # ROWS are each of our models
    # VALUES are 0/1 - 0 means no growth in m9 after gene deletion, 1 means growth in m9 after gene deletion
    final_df = pd.DataFrame(final_dict)
    final_df['strain'] = model_file_names
    final_df = final_df.set_index('strain')
    # write out
    final_df.to_csv(args.out + '_single_gene_deletions.txt', sep='\t')

if __name__ == '__main__':
    main()
