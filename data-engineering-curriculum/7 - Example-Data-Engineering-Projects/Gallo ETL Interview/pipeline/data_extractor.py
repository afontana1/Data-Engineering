import csv
import re
from urllib.request import urlopen

import pandas as pd

# import pyarrow
# import fastparquet
import requests
import traceback
import logging

valid_url_regex = re.compile(
    r"^https?://"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
    r"localhost|"  # localhost
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)


class RowToColumnOriented:
    """
    A class used for converting row oriented data to column oriented.

    ...

    Attributes
    ----------
    location: str
            location of the target dataset
    raw_data: str
            raw data download from target URL
    tabular_form: DataFrame
            tabular representation of raw data in row oriented form
    columns: list
            list of column names applicable to the dataset
    filename: str
            name of the output file
    """

    def __init__(self, location, columns, csv_filename, parquet_filename):
        self.location = self._validate_url(location)
        self.columns = columns
        self.csv_filename = csv_filename
        self.parquet_filename = parquet_filename
        self.tabular_form = None
        self.raw_data = None

    def _validate_url(self, url):
        """
        Runs basic validation on input string verifying it is a URL.

        Args:
                url: (str) URL we wish to ping.
        Returns:
                URL if valid URL else ERROR raised
        """
        if not url:
            raise Exception("Provide a URL")
        validated_url = valid_url_regex.search(url)
        if not validated_url:
            try:
                urlopen(url)
            except:
                raise Exception("Please verify that you provided a valid URL.")
        return url

    def _response_to_file(self, response, output_path):
        """
        Write response text to a csv.
        Args:
                response: (str) response string
        Return:
                None
        """
        rows = response.split("\n")
        output_path_and_name = output_path + "\\" + self.csv_filename
        with open(output_path_and_name, "w", newline="") as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(self.columns)
            for row in rows:
                records = row.split(",")
                if records:
                    csv_writer.writerow(records)
        LOGGER.info("Wrote the file to csv")
        return

    def _make_request(self, params=None):
        """
        Make request to external server.
        Args:
            url (string): Candidate URL to target
        Return:
            object (response object) or dict: if successful, return content. If else, return status code.
        """
        response = requests.get(
            self.location,
            headers={
                "Connection": "close",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
            params=params,
        )
        if not response.status_code != "200":
            LOGGER.warning("Could not acquire file")
            return {"URL": self.location, "status": response.status_code}
        LOGGER.info("Acquired file")
        self.raw_data = response.text
        return self.raw_data

    def get_data_from_source(self, output_path):
        """
        Get data from the URL provided,write to csv.

        Args:
                None
        Return:
                Dataset: (pd.DataFrame) dataframe representaion of raw data
        """
        if self.tabular_form is not None:
            return self.tabular_form
        response = self._make_request()
        if isinstance(response, dict):
            return response
        self._response_to_file(response, output_path)
        self.tabular_form = pd.read_csv(output_path + "\\" + self.csv_filename)
        return self.tabular_form

    def convert_csv_to_parquet(
        self,
        target_file_path,
        dataset=None,
        source_file_path=None,
        columns_subset=None,
        compression=None,
    ):
        """
        function to convert source csv file to target parquet file
        Args:
                dataset: (optional)
                source_file_path: (optional)
                target_file_path: (str) where to store the data.
                columns_subset: (list) subset of columns you wish to keep
                compression: (optional) compression type
        Return:
                None
        """
        if dataset:
            dataset.to_parquet(
                target_file_path + "\\" + self.parquet_filename,
                compression=compression or "UNCOMPRESSED",
                engine="fastparquet",
            )
            return

        if source_file_path and target_file_path:
            try:
                data_frame = pd.read_csv(
                    source_file_path + "\\" + self.csv_filename, usecols=columns_subset
                )
                LOGGER.info("Acquired CSV")
            except Exception:
                trace_back = traceback.format_exc()
                LOGGER.error(trace_back)
                return

            try:
                data_frame.to_parquet(
                    target_file_path + "\\" + self.parquet_filename,
                    compression=compression or "UNCOMPRESSED",
                    engine="fastparquet",
                )
                LOGGER.info("Wrote to parquet")
            except Exception:
                trace_back = traceback.format_exc()
                LOGGER.error(trace_back)
                return

    def convert_parquet_to_csv(self, target_file_path, source_file_path, columns=None):
        """
        function to convert parquet file to csv
        Args:
                source_file_path: (optional)
                target_file_path: (str) where to store the data.
                columns: (list) subset of columns you wish to keep
        Return:
                None
        """
        try:
            data_frame = pd.read_parquet(
                source_file_path + "\\" + self.parquet_filename, columns=columns
            )
            LOGGER.info("Read in parquet")
        except Exception:
            trace_back = traceback.format_exc()
            LOGGER.error(trace_back)

        try:
            data_frame.to_csv(target_file_path + "\\" + self.csv_filename, index=False)
            LOGGER.info("Wrote to csv")
        except Exception:
            trace_back = traceback.format_exc()
            LOGGER.error(trace_back)
            return
