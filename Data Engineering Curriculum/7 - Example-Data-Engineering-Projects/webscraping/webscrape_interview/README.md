# Webscrape

This collection of files contains source code used in automating the extraction, transformation, and loading of finsight data. The objective is to extract data from xml files located on the website, flatten them, and publish to a "database"; along with metadata scraped off the html. 

## Contents of each file

- **webscrape.py:** Contains the source code used to automate the web browser. Finsight data has a very dynamic web page; the HTML is generated dynamically with React. In order to extract the needed content, the web browser must be automated to load hidden and dynamically generated elements. The output is a collection of metadata, including the href linking out to the actual XML files.

- **parse.py:** Contains source code that extracts the XML content, transforms it, and flattens it into a tabular structure. The instructions specified to create a singular flat database. I decided to store each XML separately in a CSV structure since I do not have access to a relational database and it was not clear if connecting to a relational database was the intended objective. If the data needs to be used, the code can be extended to merge the separate CSVs into a common file. 

- **utils.py:** Contains utility functionality used in parse.py

## Subdirectories

- **data:** contains the metadata extracted from webscrape.py
- **flatfiles:** contains the transformed flattened files
- **raw_xml:** contains raw XML strings extracted from Finsight