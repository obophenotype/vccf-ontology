from argparse import ArgumentParser, Namespace

import pandas as pd
from utils import generate_id, read, load, search_id, extract


def crosswalk_template(crosswalk_data, vessels_data) -> pd.DataFrame:
    template = [
        {
            "Vessel": "ID",
            "Label": "LABEL",
            "overlaps": "SC overlaps some %",
            "part_of": "SC 'part_of' some %",
            "directly_supplies_drains": "SC directly_supplies_drains some %",
            "connected_to": "SC 'connected to' some %",
            "drains": "SC drains some %",
            "supplies": "SC supplies some %",
            "located_in": "SC located_in some %",
        }
    ]
    vccf_id = generate_id(2000000, 2999999)
    # print(crosswalk_data)
    for _, row in crosswalk_data.iterrows():
        if row["Relationship"] != "nan":
            r = {}
            r["Vessel"] = search_id(vessels_data, row["Vessel"])
            r["Label"] = row["Vessel"]
            r[f"{row['Relationship']}"] = row["BodySubPartID"] if row["BodySubPartID"] else next(vccf_id)
            template.append(r)
        
    return pd.DataFrame.from_records(template)

def main(args: Namespace):
    data = read(args.input)
    vessels_data = read(args.vessels, sep="\t")
    crosswalk_data = extract(data=data, columns_extract=["Vessel", "Relationship", "BodyPartID", "BodySubPart", "BodySubPartID"])
    
    template = crosswalk_template(crosswalk_data=crosswalk_data, vessels_data=vessels_data)
    load(template, args.template)
    
if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input', help="vessel - organ crosswalk input file")
    parser.add_argument('--template', help="robot template output file")
    parser.add_argument('--vessels', help="csv file listing vessels term id")
  
    args = parser.parse_args()
    main(args)