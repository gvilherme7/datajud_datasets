from datetime import datetime
import time
import re

import requests
import pandas as pd
from unidecode import unidecode

from utils import get_project_root, get_env_var


def collect_cases(query: dict[str, any], court_acronym: str) -> list[dict]:
    """
    Collects judicial case data from the DataJud API using the `search_after` pagination strategy.

    Args:
        query (dict): Elasticsearch-style query to filter cases.
        court_acronym (str):

    Returns:
        list[dict]: List of all cases returned by the API.
    """
    print("Starting data collection from the API using search_after...")

    api_key = get_env_var("DATAJUD_API_KEY")
    if not api_key:
        raise ValueError("API Key not found. See .env.example.")

    endpoint = f"https://api-publica.datajud.cnj.jus.br/api_publica_{court_acronym}/_search"
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json"
    }

    query['sort'] = [{"@timestamp": {"order": "asc"}}]
    query['size'] = 10000

    all_cases = []
    last_sort_value = None

    while True:
        if last_sort_value:
            query["search_after"] = last_sort_value

        try:
            response = requests.post(endpoint, headers=headers, json=query, timeout=120)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request failed. Cause: {e}")
            break

        hits = response_data.get("hits", {}).get("hits", [])
        if not hits:
            break

        for hit in hits:
            all_cases.append(hit['_source'])

        last_sort_value = hits[-1].get("sort")
        total_collected = len(all_cases)
        estimated_total = response_data.get("hits", {}).get("total", {}).get("value", 0)
        print(f"Collected {total_collected} out of approximately {estimated_total} cases...")

        time.sleep(1)

    print(f"Data collection completed. Total of {len(all_cases)} raw cases found.")
    return all_cases


def process_and_save_csv(raw_data: list[dict], file_name: str):
    """
    Processes raw case data into a structured dataset and saves it as a CSV file.

    Args:
        raw_data (list): List of raw case data dictionaries.
        file_name (str): Name of the CSV file to be saved (without path).
    """
    print("\nStarting data processing and dataset creation...")

    if len(raw_data) < 1:
        print("No data to process.")
        return

    cleaned_dataset = []
    for case in raw_data:
        class_info = case.get('classe', {})
        court = case.get('orgaoJulgador', {})
        subjects = case.get('assuntos', [])
        motions = case.get('movimentos', [])

        subject_names = "|".join([
            subject.get('nome', '')
            for subject in subjects if isinstance(subject, dict)
        ]) if subjects else ""

        duration_days = None
        last_motion_date = None
        last_motion_code = None
        last_motion_name = None

        if motions:
            valid_motions = [m for m in motions if m and m.get('dataHora')]
            if valid_motions:
                motion_dates = [
                    datetime.fromisoformat(motion.get('dataHora').replace('Z', '+00:00'))
                    for motion in motions if motion and motion.get('dataHora')
                ]
                if motion_dates:
                    start_date = min(motion_dates)
                    end_date = max(motion_dates)
                    duration_days = (end_date - start_date).days

                    last_mot_dict = max(valid_motions, key=lambda mov: mov['dataHora'])
                    last_motion_date = last_mot_dict.get('dataHora')
                    last_motion_code = last_mot_dict.get('codigo')
                    last_motion_name = last_mot_dict.get('nome')

        row = {
            "case_number": case.get('numeroProcesso'),
            "filing_date": case.get('dataAjuizamento'),
            "court": case.get('tribunal'),
            "degree": case.get('grau'),
            "secrecy_level": case.get('nivelSigilo'),
            "class_code": class_info.get('codigo'),
            "class_name": class_info.get('nome'),
            "court_code": court.get('codigo'),
            "court_name": court.get('nome'),
            "municipality_ibge": court.get('codigoMunicipioIBGE'),
            "subject_names": subject_names,
            "case_duration_days": duration_days,
            "last_motion_date": last_motion_date,
            "last_motion_code": last_motion_code,
            "last_motion_name": last_motion_name
        }
        cleaned_dataset.append(row)

    df = pd.DataFrame(cleaned_dataset)
    df.to_csv(f"{get_project_root()}/data/{file_name}", index=False, encoding='utf-8-sig')

    print(f"\nDataset successfully saved as '{file_name}'.")
    print(f"The dataset contains {len(df)} rows and {len(df.columns)} columns.")


if __name__ == "__main__":
    COURT_ACRONYM = "tjsc"
    CITY_NAME = "tubarao"
    CITY_IBGE_CODE = "4218707"
    COURT_NAME = "1ª Vara Cível"

    cleaned_court_name = (
        re.sub(r'[^a-zA-Z0-9\s]', '', unidecode(COURT_NAME)).replace(" ", "_").lower()
    )
    file_name = f"{COURT_ACRONYM}_{CITY_NAME}_{cleaned_court_name}.csv"

    specific_court_query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"orgaoJulgador.codigoMunicipioIBGE": CITY_IBGE_CODE}},
                    {"match_phrase": {"orgaoJulgador.nome": COURT_NAME}}
                ]
            }
        }
    }

    collected_data = collect_cases(specific_court_query, COURT_ACRONYM)
    process_and_save_csv(collected_data, file_name) 