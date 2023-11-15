import requests
import logging

logging.basicConfig(level=logging.INFO)


def get_file(url: str, file: str) -> bool:
    r = requests.get(url, allow_redirects=True)
    if r.ok:
        logging.info(f"Request got valid response : {r.status_code}. Content sample : {r.content[:100]}")
        open(file, 'wb').write(r.content)
    else:
        logging.error(f"Request failed at path : {url}. Full content : {r.content}")
    return r.ok


def get_gouv_data(
        day: str = "01", 
        month: str = "01", 
        year: str = "2023", 
        save_folder_path: str = "./data/raw", 
        base_url: str = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel", 
        file_prefix: str = "FR_E2"
) -> bool:
    file_name = f"{file_prefix}_{year}-{month}-{day}.csv"
    full_url = f"{base_url}/{year}/{file_name}"
    full_save_path = f"{save_folder_path}/{file_name}"
    response_status = get_file(full_url, full_save_path)
    return response_status
    

def get_gouv_metadata(
        url: str = "https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/#/resources/eb87c56c-dea9-4377-a1e7-03ada59d3043",
        save_folder_path: str = "./data/raw"
) -> bool:
    """
    TO-DO: get stable link, current one might be linked to the current update at 15/11/2023 
    """
    full_save_path = f"{save_folder_path}/ineris_metadata.xls"
    response_status = get_file(url, full_save_path)
    return response_status


if __name__ == "__main__":
    # get_gouv_data()
    get_gouv_metadata()
