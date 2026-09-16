"""
The functionality below is for:
- reading the metadata
- making external request to source server
- extracting xml and writing to local director
- reading the xml and parsing the <asset> tag
- converting the asset tag in each xml doc to a list of json records
- converting each json record to a csv row, writing to file
"""

from dataclasses import dataclass
import xml.etree.ElementTree as ET
from lxml import etree
import requests
import re
import json
import os
import csv
import io

from utils import is_valid_url, make_request


@dataclass
class record:
    sector: str
    name: str
    file_date: str
    urls: list

    def remove_urls(self):
        """remove unwanted urls from urls list"""

        def identify_url(url):
            """identify xml url"""
            extension = ""
            for char in url[::-1]:
                extension += char
                if extension[::-1] == ".xml":
                    return True
            return False

        self.urls = [url for url in self.urls if identify_url(url)]


def read_data():
    """return list containing each row as a record"""
    records = []
    path = os.getcwd() + "\Data\{}"
    subdirectory = os.getcwd() + "\Data"

    for file in os.listdir(subdirectory):
        path_to_file = path.format(file)
        with open(path_to_file.format(file), "r") as infile:
            row = json.load(infile)
            for element in row:
                recored_type = record(**element)
                recored_type.remove_urls()
                records.append(recored_type)
    return records


def write_xml_to_disc(fname, xmlString):
    """Write XML file to disc, in memory is too large"""
    with open(
        r"C:\\Users\\Aj\\Documents\\project\\raw_xml\\{}.xml".format(fname), "w"
    ) as out:
        out.write(xmlString)
    return


def parse_xml_file(file):
    """Parse the xml tree from the file path
    Use for AUTO data where there is no nested structure.
    """
    root = etree.parse(r"raw_xml\test.xml").getroot()
    out = []
    for el in root:
        temp = {}
        for child in el.getchildren():
            _, _, child.tag = child.tag.rpartition("}")
            temp[child.tag] = child.text
        out.append(temp)
    return out


def parse_xml_file_recursive(file):
    data = []

    def recurse_through_tree(node):
        """Parse the xml tree from the file path"""
        for el in node:
            if list(el):
                recurse_through_tree(el)
            else:
                _, _, el.tag = el.tag.rpartition("}")
                out[el.tag] = el.text

    root = etree.parse(r"raw_xml\{}.xml".format(file)).getroot()
    for node in root.getchildren():
        out = {}
        recurse_through_tree(node)
        data.append(out)
    return data


def write_xml_to_csv(listOfRecords, sector, fileName, date):
    """Write unpacked xml to flat file"""
    with open(
        r"flatfiles\{}\{}_{}.csv".format(sector, sector + "_" + fileName, date), "w"
    ) as f:
        writer = csv.writer(f)
        header, header_set = [], set()
        rows = []
        for row in listOfRecords:
            for key in row:
                if key not in header_set:
                    header_set.add(key)
                    header.append(key)
            rows.append([row.get(col, "") for col in header])

        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    return


def remove_spaces(string):
    """Format String"""
    return string.replace(" ", "_").replace(",", "")


def process(records):
    """process the records
    Ignore the metadata for the auto xml, can save to raw if needed
    """
    check_records = []
    for record in records:
        print("parsing record")
        if not record.urls[0]:
            continue
        response = make_request(record.urls[0])
        if isinstance(response, (str, dict)):
            check_records.append(record)
            continue
        name = remove_spaces(record.name)
        date = remove_spaces(record.file_date)
        fname = record.sector + "_" + name + "_" + date
        write_xml_to_disc(fname, response.text)
        if record.sector == "AUTO":
            parsed_contents = parse_xml_file(fname)
        else:
            parsed_contents = parse_xml_file_recursive(fname)
        write_xml_to_csv(parsed_contents, record.sector, name, date)


if __name__ == "__main__":
    records = read_data()
    process(records)
