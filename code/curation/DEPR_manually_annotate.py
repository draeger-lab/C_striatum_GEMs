#%% imports and functions
from libsbml import *
import pandas as pd

metabol_db_dict = {'BIGG': 'bigg.metabolite/', 
                   'BRENDA': 'brenda/', 
                   'CHEBI': 'chebi/',
                   'INCHI': 'inchikey/', 
                   'KEGG': 'kegg.compound/', 
                   'METACYC': 'metacyc.compound/',
                   'MXNREF': 'metanetx.chemical/', 
                   'SEED':'seed.compound/', 
                   'UPA': 'unipathway.compound/', 
                   'HMDB': 'hmdb/', 
                   'REACTOME': 'reactome/',
                   'BIOCYC': 'biocyc/',
                   'PUBCHEM': 'pubchem.compound/'}

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

def metab_only1_ann(model):
    spe = model.getListOfSpecies()

    only_one = [] #safe metab with only BiGG annotation
    for sb in spe:
        if sb.isSetId():
            pid = sb.getId()
            if sb.getCVTerm(0).getNumResources() == 1:
                only_one.append(pid)
                
    return only_one

def add_cv_term_from_notes_species(entry, db_id, metab):
    cv = CVTerm()
    cv.setQualifierType(BIOLOGICAL_QUALIFIER)
    cv.setBiologicalQualifierType(BQB_IS)
    cv.addResource('https://identifiers.org/'+ metabol_db_dict[db_id]+entry)
    metab.addCVTerm(cv)

def add_annotation_from_table(model, table):
    for met in table['BIGG']:
        for comp in ['_c', '_e', '_p']:
            try:
                metab = model.getSpecies('M_' + met + comp)
                metab.unsetAnnotation()
                for (columnName, columnData) in table.loc[table['BIGG'] == met].iteritems():
                    for entry in columnData.values:
                        if not entry == 0:
                            add_cv_term_from_notes_species(str(entry), str(columnName), metab)
                print(metab.getAnnotationString())
            except (AttributeError):
                print(met + comp + ' not in model')

#%% look for metab that need annotation to extend manual_annotations.xlsx
path = '../models/Cstr_14.xml'
model = load_model_libsbml(path)
print(metab_only1_ann(model))

#%% load manual_annotations.xlsx
man_ann = pd.read_excel('../data/manual_curation.xlsx', 'metab').drop(['Name', 'FORMULA', 'Notiz'], axis=1).fillna(0)
man_ann['PUBCHEM'] = man_ann['PUBCHEM'].astype(int)
man_ann

#%% annotate all models using the manually curated table manual_annotations.xlsx
modelpaths = ['../models/Cstr_14.xml', '../models/Cstr_15.xml', '../models/Cstr_16.xml', '../models/Cstr_17.xml']

for path in modelpaths:
    model = load_model_libsbml(path)
    add_annotation_from_table(model, man_ann)
    writeSBMLToFile(model.getSBMLDocument(),path)