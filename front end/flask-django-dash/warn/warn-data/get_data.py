import requests
import os
import pathlib

URLS = {
    "2023": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2022-to-06-30-2023.pdf",
    "2022": "https://edd.ca.gov/siteassets/files/jobs_and_training/pubs/warn-report-for-7-1-2021-to-06-30-2022.pdf",
    "2021": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2020-to-06-30-2021.pdf",
    "2020": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2019-to-6-30-2020.pdf",
    "2019": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2018-to-06-30-2019.pdf",
    "2018": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2017-to-06-30-2018.pdf",
    "2017": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2016-to-06-30-2017.pdf",
    "2016": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn-report-for-7-1-2015-to-06-30-2016.pdf",
    "2015": "https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warnreportfor7-1-2014to06-30-2015.pdf",
}

CURRENT_DIR = str(pathlib.Path(__file__).parent.resolve())
DATA_DIRECTORY = os.path.join(CURRENT_DIR, "data")


def get_data(url: str) -> requests.models.Response:
    """Get raw data"""
    try:
        response = requests.get(url)
    except Exception as e:
        raise (e)
    if response.status_code != 200:
        raise Exception("status code not 200, check the problem")
    return response


def write_to_file(name: str, response: requests.models.Response) -> bool:
    with open(f"{DATA_DIRECTORY}\{name}.pdf", "wb") as out:
        out.write(response.content)
    return True


if __name__ == "__main__":
    """TODO: Make Async for fun"""
    for year, url in URLS.items():
        file_name = f"warn-{year}"
        print(file_name)
        response = get_data(url=url)
        write_to_file(file_name, response)
