"""
Script to transform vesse_organ_crosswalk CSV file into ROBOT templ
"""
from argparse import ArgumentParser, Namespace

import pandas as pd
from utils import extract, generate_id, load, read, search_id


def crosswalk_template(crosswalk_data, vessels_data) -> pd.DataFrame:
    template = [
        {
            "Vessel": "ID",
            "TYPE": "TYPE",
            "Label": "LABEL",
            "overlaps": "SC overlaps some %",
            "part_of": "SC 'part of' some %",
            "directly_supplies_drains": "SC 'directly supplies and drains' some %",
            "connected_to": "SC 'connected to' some %",
            "drains": "SC 'vessel drains blood from' some %",
            "supplies": "SC 'vessel supplies blood to' some %",
            "located_in": "SC 'located in' some %",
        }
    ]

    vccf_id = generate_id(2000000, 2999999)
    new_vessels = {}
    for _, row in crosswalk_data.iterrows():
        if str(row["Relationship"]) != "nan":
            vessel_id = search_id(vessels_data, row["Vessel"])

            if "NOTFOUND" in vessel_id:
                if row["Vessel"] not in new_vessels:
                    new = next(vccf_id)
                    new_vessels[row["Vessel"]] = new
                    vessel_id = f"VCCF:{new}"
                else:
                    vessel_id = f"VCCF:{new_vessels[row['Vessel']]}"
            r = {}
            r["Vessel"] = vessel_id
            if row["Vessel"] in new_vessels:
                r["Label"] = row["Vessel"]
            if str(row["BodyPartID"]) != "nan":
                r[f"{row['Relationship']}"] = row["BodySubPartID"]
            else:
                r[f"{row['Relationship']}"] = f"VCCF:{next(vccf_id)}"
                r["Label"] = row["BodySubPart"]
            template.append(r)

    return pd.DataFrame.from_records(template)


def main(args: Namespace):
    data = read(args.input)
    vessels_data = read(args.vessels, sep="\t")
    crosswalk_data = extract(data=data, columns_extract=[
        "Vessel",
        "Relationship",
        "BodyPartID",
        "BodySubPart",
        "BodySubPartID"
    ])

    template = crosswalk_template(
        crosswalk_data=crosswalk_data,
        vessels_data=vessels_data
    )
    load(template, args.template)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', help="vessel - organ crosswalk input file")
    parser.add_argument('--template', help="robot template output file")
    parser.add_argument('--vessels', help="csv file listing vessels term id")

    args = parser.parse_args()
    main(args)
