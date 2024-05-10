
![Build Status](https://github.com/obophenotype/vccf-ontology/workflows/CI/badge.svg)
# STATUS - EXPERIMENTAL DO NOT USE
# Vasculature Common Coordinate Framework Ontology

## Pipeline workflow

1. Use a [DOSDP](src/patterns/dosdp-patterns/vessel.yaml) to define all vessels available in the [datasource](https://github.com/hubmapconsortium/hra-vccf/blob/main/Vessel.csv). A python script is used to generate the [data](src/patterns/data/default/vessel.tsv) for the DOSDP.
   - [label, human_label] The colum `VesselBaseName` is used for the VCCF term label and for  `oio:obo_foundry_uniquename` annotation, adding "(Human)". We use this column as label because it's the vessel name without the “#N” at the end. This applies to vessels with more than one `BranchesFrom`. However, in cases where there is a specific number of vessels in the body, the `VesselBaseName` includes a number for each different vessel. In UBERON, these cases should be added only one term. **TODO: Remove vessels with numbers**.
   - [parent] The column `VesselTypeID` is used for the vessel classification. Possible values are, as UBERON term, heart chamber, artery, arteriole, capillary, venule, vein, or sinus. In the cases there isn't a matching UBERON term for the vessel, defined in the column `UBERON`. In other words, when the vessel exists in FMA or no matching term is available. **TODO: add `VesselTypeID` for all cases**. 
     - When `VesselTypeID` is `heart chamber` the values in `BranchesFrom` and `Vessel` are the same, which in fact are not vessels. e should not add the `BranchesFrom` relationship because it's the same as in `Vessel` which is not true. It should include only the `VesselTypeID` as parent and link to the matching UBERON term. **TODO: Remove relationship in these cases**. **TODO: Remove heart chamber type terms from data related to vessel DP?**.
   -  [location] The column `BodyPart` is used for a simplified definition generation. In some cases, this can be redundant with data available in the [crosswalk table](https://github.com/hubmapconsortium/hra-vccf/blob/main/VesselOrganCrosswalk.csv) which defines specific relationship between the vessel and the tissue. **TODO: Improve the use of this column in the DOSDP**.
   -  [xrefs] The columns `ReferenceURL` and `ReferenceDOI` are used as xref for the definition in the pattern. Some values in `ReferenceURL` are the URL for the UBERON matching term. These cases the reference is empty. When the `ReferenceURL` is a PMC publication url, it's transformed to PMID. **TODO: Remove DOI if `ReferenceURL` is from PMC publication**. **TODO: Search for DOI in radiopaedia cases**
   -  [synonym, synonym_xref] The column `FMALabel` and `FMA` are used as exact synonym and synonym xref, respectively, when available.
   -  [taxon] The taxon NCBITaxon:9606 (Homo Sapiens) is asserted in all VCCF terms as `present in taxon` relationship.
1. [Robot template](src/templates/vessel_relation.tsv) to create relationship between vessels defined in the [datasource](https://github.com/hubmapconsortium/hra-vccf/blob/main/Vessel.csv).
   - This uses the column `BranchesFrom`, which means the “parent” vessel that is one step closer to the heart. For the ontology, we use `connecting branch of`.
     - Following data source documentation, for veins it is `drains to` rather than `connecting branch of`. **TODO: Define relationship by `VesselType`**.
1. [Robot template](src/templates/vessel_organ_crosswalk.tsv) to create relation between vessel and tissue. The data source is the [crosswalk table](https://github.com/hubmapconsortium/hra-vccf/blob/main/VesselOrganCrosswalk.csv). 
   - [Vessel] The column `Vessel` is the VCCF terms created in the DOSDP. The search is done by the label.
   - [relationships] For each relationship in the `Relationship` column, is added in the template. **TODO: When there isn't a matching UBERON term in the column `BodySubPartID`, use `BodyPartID` which is the organ. However, we need to discuss what to do in cases `BodyPart` is angiosome**.

## Versions

### Stable release versions

The latest version of the ontology can always be found at:

[vccf.owl](vccf.owl)


### Editors' version

Editors of this ontology should use the edit version, [src/ontology/vccf-edit.owl](src/ontology/vccf-edit.owl)

## Contact

Please use this GitHub repository's [Issue tracker](https://github.com/obophenotype/vccf-ontology/issues) to request new terms/classes or report errors or specific concerns related to the ontology.

## Acknowledgements

This ontology repository was created using the [Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit).
