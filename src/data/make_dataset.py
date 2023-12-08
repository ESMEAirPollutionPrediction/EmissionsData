import requests
import logging
import datetime
import csv

logging.basicConfig(level=logging.INFO)


def get_file(url: str, file: str) -> bool:
    r = requests.get(url, allow_redirects=True)
    if r.ok:
        logging.info(f"Request got valid response : {r.status_code}. Content sample : {r.content[:100]}")
        open(file, 'wb').write(r.content)
    else:
        logging.error(f"Request failed at path : {url}. Full content : {r.content}")
    return r.ok


def get_gouv_data_and_metadata(
        save_folder_path: str = "./data/raw",
        base_url: str = "https://files.data.gouv.fr/lcsqa/concentrations-de-polluants-atmospheriques-reglementes/temps-reel",
        file_prefix: str = "FR_E2",
        metadata_url: str = "https://www.data.gouv.fr/fr/datasets/donnees-temps-reel-de-mesure-des-concentrations-de-polluants-atmospheriques-reglementes-1/#/resources/eb87c56c-dea9-4377-a1e7-03ada59d3043"
) -> bool:
    today = datetime.date.today()
    start_date = datetime.date(2021, 1, 1)
    current_date = start_date

    metadata_file_name = "metadata.xls"
    metadata_full_url = metadata_url
    metadata_full_save_path = f"{save_folder_path}/{metadata_file_name}"
    metadata_response_status = get_file(metadata_full_url, metadata_full_save_path)
    if not metadata_response_status:
        return False

    data_file_name = "data.csv"
    data_full_save_path = f"{save_folder_path}/{data_file_name}"
    with open(data_full_save_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Pollutant", "Value"])

        while current_date <= today:
            day = str(current_date.day).zfill(2)
            month = str(current_date.month).zfill(2)
            year = str(current_date.year)
            file_name = f"{file_prefix}_{year}-{month}-{day}.csv"
            full_url = f"{base_url}/{year}/{file_name}"
            full_save_path = f"{save_folder_path}/{file_name}"
            response_status = get_file(full_url, full_save_path)
            if not response_status:
                return False

            # Read data from the downloaded file and write it to the combined CSV file
            with open(full_save_path, 'r') as datafile:
                reader = csv.reader(datafile)
                next(reader)  # Skip the header row
                for row in reader:
                    writer.writerow([f"{year}-{month}-{day}", row[0], row[1]])

            current_date += datetime.timedelta(days=1)

    return True

get_gouv_data_and_metadata()
