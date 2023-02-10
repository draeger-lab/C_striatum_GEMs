# Virtual Metabolic Human

The VMH released a new version of all their models in the beginning of this year. This folder is dedicated to the model and analysing it which is why everything is kept here since it is not directly related to the curating efforts that I did with my own models.

**Argument for a new model**
A single genome-scale metabolic model (GEM) of C. striatum is available. This model represents the type strain ATCC 6940, it has a MEMOTE score of 88% and was created as a part of the Virtual Metabolic Human (VMH). Most models within the VMH are used as basis to build simulatable microbiomes (f. ex. of the gut). However, a manually curated and high quality GEM model of C. striatum was not available. VMH models also all use specific entity identifiers which are sometimes overlapping with BiGG identifiers but not always. The VMH model also holds erroneous annotations with NaN IDs or non-existing INCHI-keys. None of the GeneProducts were annotated and some of the reaction where only annotated with their respective SBO term.

**Comparison to my models**
- The new version of the model has a MEMOTE score of 88% and is better annotated. It has the following scope: 1097 metabolites, 1235 reactions and 767 genes and a metabolic coverage of 1.61.
- (compare to starting stats of my model - memote score is 69% and it has 1396 metabolites, 2021 reactions and 773 genes, metabolic coverage above 2)


**VMH model properties**

- This model also has empty annotations as follows and the metabolite IDs are VMH based `(M_13mmyrsACP__91__c__93__)`.

```xml
<rdf:li rdf:resource="http://identifiers.org/bigg.metabolite/NaN"/>
<rdf:li rdf:resource="http://identifiers.org/biocyc/NaN"/>
```

- Some INCHI Keys are not accessible: 

```xml
<rdf:li rdf:resource="http://identifiers.org/inchi/InChI=1S/C24H49O9P/c1-2-3-4-5-6-7-8-9-10-11-12-13-14-15-16-17-24(28)31-19-23(27)21-33-34(29,30)32-20-22(26)18-25/h22-23,25-27H,2-21H2,1H3,(H,29,30)/p-1"/>
```

- It has groups which are named but the ID is not descriptive

```xml
<groups:group sboTerm="SBO:0000633" groups:id="group16" groups:name="CoA catabolism" groups:kind="partonomy">
```

- The genes (GeneProducts) are not annotated

```xml
<fbc:geneProduct metaid="G_g__46__1991__46__peg__46__1098" sboTerm="SBO:0000243" fbc:id="G_g__46__1991__46__peg__46__1098" fbc:label="g.1991.peg.1098"/>
```

- Some reactions are only annotated with their respective SBO term.

- The biomass reaction has specified stoichiometries

```xml
<speciesReference species="M_pheme__91__c__93__" stoichiometry="0.0030965" constant="true"/>
```

- there are 110 orphans and 74 deadends