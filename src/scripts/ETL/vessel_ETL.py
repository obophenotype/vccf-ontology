import argparse

import pandas as pd
from utils import extract, generate_id, load, read, search_id, transform_id


def transform_pattern(data: pd.DataFrame) -> pd.DataFrame:
    # columns_pattern = ["defined_class", "label", "human_label", "parent", "location", "xrefs", "synonym", "synonym_xrefs", "taxon"]
    data_pattern = []
    data = data.drop_duplicates(['VesselBaseName'])
    vccf_id = generate_id(1000000, 1999999)
    for _, row in data.iterrows():
        r = {}
        r["defined_class"] = f'VCCF:{next(vccf_id)}'
        r["label"] = row['VesselBaseName'].rstrip()
        r["human_label"] = f'{row["VesselBaseName"].rstrip()} (Human)'

        if not pd.isna(row['UBERON']):
            r['parent'] = row['UBERON']
        elif 'fma' not in row['VesselTypeID']:
            r['parent'] = row['VesselTypeID']

        r['location'] = row['BodyPart']

        references = []
        if 'http' in row['ReferenceURL'] and 'UBERON' not in row['ReferenceURL']:
            references.append(row['ReferenceURL'])
        if not pd.isna(row['ReferenceDOI']):
            references.append(f'DOI:{row["ReferenceDOI"]}')

        r['xrefs'] = '|'.join(references)

        r['synonym'] = row['FMALabel']
        if not pd.isna(row['FMA']):
            r['synonym_xrefs'] = transform_id(row['FMA'])
        r['taxon'] = "http://purl.obolibrary.org/obo/NCBITaxon_9606"
        data_pattern.append(r)

    return pd.DataFrame.from_records(data_pattern)


def transform_template(
    pattern_data: pd.DataFrame,
    template_data: pd.DataFrame
) -> pd.DataFrame:
    data_template = [{"Vessel": "ID", "branches from": "SC 'connected to' some %"}]
    for _, row in template_data.iterrows():
        r = {}
        r['Vessel'] = search_id(pattern_data, row['VesselBaseName'])
        r['branches from'] = search_id(pattern_data, row['BranchesFrom'])
        data_template.append(r)

    return pd.DataFrame.from_records(data_template)


def main(args):
    data = read(args.input)
    pattern_data = extract(data=data, columns_extract=[
        "VesselBaseName", "VesselType", "VesselTypeID", "ReferenceURL", "ReferenceDOI",
        "BodyPart", "BodyPartID", "UBERON", "UBERONLabel", "FMALabel", "FMA"
        ]
                           )
    pattern_data = transform_pattern(pattern_data)
    load(pattern_data, args.pattern)

    template_data = extract(data=data, columns_extract=["BranchesFrom", "VesselBaseName"])
    template_data = transform_template(pattern_data, template_data)
    load(template_data, args.template)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='vessel input file')
    parser.add_argument('--pattern', help='dos-dp pattern output file')
    parser.add_argument('--template', help='robot template output file')

    args = parser.parse_args()
    main(args)
