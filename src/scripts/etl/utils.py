from pathlib import Path

import pandas as pd
import requests


def read(input, sep=","):
    return pd.read_csv(input, encoding="latin-1", sep=sep)


def load(data: pd.DataFrame, file: Path):
    data.to_csv(file, sep='\t', index=False)


def search_id(data, term_label):
    filter_label = data[data["label"] == term_label.strip()]
    if len(filter_label):
        return filter_label['defined_class'].values[0]

    return "NOTFOUND"


def generate_id(start_range, end_range):
    for i in range(start_range, end_range, 1):
        yield str(i)


def transform_id(term):
    split = term.lower().split('a')
    return f'FMA:{split[1]}'


def extract(data: pd.DataFrame, columns_extract: list) -> pd.DataFrame:
    return data[columns_extract]  # type: ignore


def convert_pmcid(url):
    BASE_URL = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    pmcid = url.split('/')[-2]
    response = requests.get(BASE_URL, params={"ids": pmcid, "format": "json"})
    return f"PMID:{response.json()['records'][0]['pmid']}"
